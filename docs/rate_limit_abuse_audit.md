# Rate Limit / Abuse Protection Audit

## Контекст проверки

В рамках аудита выполнены:

- `python -m pytest` -> `90 passed`
- `./scripts/check-backend.ps1` -> `passed`

Это подтверждает, что текущая backend-база стабильна, а выводы ниже относятся к реально рабочему состоянию приложения.

## Что уже реализовано

### Базовый rate limiter

Текущая реализация находится в `backend/app/core/rate_limit.py`.

Механика:

- ключ формируется как `rl:{scope}:{request.url.path}`
- счётчик хранится в Redis
- используется `INCR`
- при первом обращении выставляется `EXPIRE 60`
- лимит берётся из `APP_RATE_LIMIT_PER_MINUTE`
- при превышении лимита выбрасывается `AppException(code=RATE_LIMITED, message_key="errors.common.rate_limited", status_code=429)`

Конфигурация по умолчанию:

- `APP_RATE_LIMIT_PER_MINUTE=120`

### Защита auth endpoint'ов

`backend/app/api/routes/v1/auth.py` использует отдельный scope для каждого auth endpoint:

- `auth_register`
- `auth_login`
- `auth_refresh`
- `auth_logout`
- `auth_oauth`

Ключ строится через `_client_key(request, scope)` и основан на `request.client.host`, то есть защита auth сейчас фактически `per-IP`.

### Защита user-scoped mutating endpoint'ов

Во многих защищённых endpoint'ах используется ключ вида `user:{current_user.id}`. Это применяется, в частности, в:

- `goals`
- `barcodes`
- `meals.create`
- `meals.analysis`
- `uploads.init`
- `uploads.complete`
- `reports`
- `recommendations`
- `weights`
- `meal_plans`

Из этого следует, что state-changing и potentially expensive пути частично защищены `per-user` лимитом.

### Response envelope при блокировке

При превышении лимита backend возвращает стандартный error envelope через централизованный exception handler:

- HTTP `429`
- `error.code = RATE_LIMITED`
- `message_key = errors.common.rate_limited`

Это согласовано с общей моделью ошибок приложения.

## Что работает хорошо

### Auth и expensive endpoint'ы хотя бы частично защищены

Критичные для abuse surface пути не оставлены полностью открытыми:

- login/register/refresh/logout защищены
- upload init/complete защищены
- meal analysis endpoint защищён
- barcode lookup защищён

Это уже снижает риск простого flood abuse в базовом MVP/production-lite сценарии.

### Limiter не меняет API-контракт

Rate limit rejection вписывается в существующую error model и не требует отдельной обработки на уровне transport формата.

### Redis degradation не валит backend

Если Redis недоступен, limiter не ломает request path и backend продолжает обслуживать запросы. Для availability это удобно.

## Ключевые пробелы и риски

### 1. Fallback при отказе Redis работает в режиме silent fail-open

В `enforce_user_rate_limit()`:

- любые `RedisError` подавляются
- limiter просто `return`
- запрос пропускается дальше без ограничения

Это означает:

- при потере Redis весь rate limiting фактически отключается
- пользователи и боты получают неограниченный доступ к защищённым endpoint'ам
- код не пишет явное structured событие о degraded limiter path

Это главный abuse-risk текущей реализации.

### 2. Нет per-IP защиты для большинства authenticated endpoint'ов

После аутентификации лимиты в основном строятся только по `user_id`.

Риски:

- одна и та же IP-адресная точка может распределять нагрузку по множеству аккаунтов
- отсутствует дополнительный network-level shield для brute-force / scripted abuse после получения токенов
- нет составного ключа вроде `user + ip`

Для auth endpoint'ов используется только IP, а для protected business endpoint'ов в основном только user. Гибридной стратегии сейчас нет.

### 3. Coverage limiter'ом неполное и неоднородное

Лимитирование применяется не ко всем endpoint'ам.

Примеры endpoint'ов без явного limiter'а:

- `GET /api/v1/me`
- `PATCH /api/v1/me/profile`
- `PATCH /api/v1/me/locale`
- `GET /api/v1/settings`
- `PATCH /api/v1/settings`
- `GET /api/v1/meals`
- `GET /api/v1/meals/{meal_id}`
- `PATCH /api/v1/meals/{meal_id}`
- `DELETE /api/v1/meals/{meal_id}`
- `GET /api/v1/localization/locales`
- `POST /api/v1/localization/messages`

Это не обязательно ошибка для каждого пути, но означает отсутствие единой abuse policy по API surface.

### 4. Лимит глобальный и одинаковый для разных классов операций

Сейчас используется один общий параметр:

- `APP_RATE_LIMIT_PER_MINUTE`

Он одинаково влияет на:

- login
- upload init
- upload complete
- meal analysis
- simple CRUD updates

Это слишком грубо для production hardening. Более дорогие пути, особенно `meals/analysis`, обычно требуют существенно более жёстких ограничений, чем обычный CRUD.

### 5. Нет observability для blocked/degraded limiter path

Хотя общий exception logging уже добавлен, в самом limiter'е нет специальных structured logs для:

- successful block (`429`)
- Redis unavailable / limiter degraded
- high-cardinality hot keys
- repeated auth abuse from same client IP

Итог:

- `429` будут видны только как общие `AppException` записи
- silent Redis degradation почти не видна операционно
- нет прикладного сигнала, что защита отключилась

### 6. Нет стандартных headers для клиента

В текущей реализации нет ответа с:

- `Retry-After`
- `X-RateLimit-*`

Это не ломает контракт, но ухудшает client-side retry/backoff behavior и наблюдаемость на стороне мобильного приложения.

## Защита ключевых abuse-путей

### Auth

Статус:

- есть `per-IP` лимит на register/login/refresh/logout/oauth
- это лучше, чем отсутствие limiter'а

Пробелы:

- нет дифференциации по endpoint severity
- нет явных anti-bruteforce escalation rules
- нет отдельной observability по auth abuse

### Meal analysis / OpenAI path

Статус:

- `POST /api/v1/meals/analysis` лимитируется по `user_id`
- это защищает expensive AI path на базовом уровне

Пробелы:

- лимит не отделён от обычных CRUD path'ов
- нет более жёсткой политики для AI-cost endpoint'а
- при отказе Redis ограничение исчезает полностью

### Upload init / complete

Статус:

- оба upload endpoint'а лимитируются по `user_id`

Пробелы:

- нет отдельной политики для upload abuse
- нет явной защиты по IP на случай mass-account abuse
- Redis fail-open выключает защиту полностью

## Redis dependency status

Текущая зависимость от Redis жёсткая по механике и мягкая по поведению:

- limiter полностью зависит от Redis для подсчёта
- при старте приложения Redis `ping()` логируется
- при недоступности Redis startup не падает
- при runtime ошибке Redis limiter silently bypasses check

Это удобно для availability, но с точки зрения abuse protection слишком permissive.

## Логирование и error visibility

### Что есть

- `429 RATE_LIMITED` проходит через централизованный exception handler
- request/error logging middleware логирует request path и status code
- startup логирует `redis ping succeeded` / `redis ping failed`

### Чего не хватает

- отдельного limiter logger event на `rate_limit_exceeded`
- отдельного limiter logger event на `rate_limiter_degraded`
- корреляции hot IP / hot user key
- счётчиков/метрик для blocked requests

## Покрытие тестами

### Что видно сейчас

По текущему `tests/` нет явного покрытия limiter behavior для сценариев:

- request allowed under threshold
- request blocked over threshold
- Redis unavailable -> graceful degradation
- envelope correctness specifically for `429`

То есть функционально limiter присутствует, но regression safety вокруг него практически отсутствует.

Это особенно важно, потому что текущая fail-open логика очень чувствительна к незаметным изменениям.

## Итоговая оценка

Текущую систему rate limiting можно оценить как `partially ready`.

Сильные стороны:

- limiter есть
- Redis-backed window реализован
- auth, upload и meal analysis уже прикрыты
- response envelope на `429` согласован

Основные production gaps:

- silent fail-open при отказе Redis
- отсутствие единой abuse policy по endpoint'ам
- отсутствие endpoint-specific limits
- слабая observability limiter paths
- почти полное отсутствие тестов на limiter behavior

## Recommended Next Task

Рекомендуемый следующий шаг: внедрить structured rate-limit hardening без изменения API-контракта:

- добавить explicit logging для `rate_limit_exceeded` и `rate_limiter_degraded`
- покрыть тестами allowed / blocked / Redis unavailable scenarios
- выделить отдельные лимиты хотя бы для `auth`, `meals/analysis` и `uploads`
