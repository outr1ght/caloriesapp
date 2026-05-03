# Auth / Session Security Audit

## Контекст проверки

В рамках аудита выполнены:

- `python -m pytest` -> `101 passed`
- `./scripts/check-backend.ps1` -> `passed`

Это подтверждает, что backend находится в рабочем состоянии, а выводы ниже относятся к реально проходящей test/runtime базе.

## Что уже реализовано

### JWT access token

В `backend/app/core/security.py` access token создаётся через `create_access_token()`.

Текущие claims:

- `sub` - user id
- `token_type` - `access`
- `iat`
- `exp`
- `jti`

Параметры:

- подпись: `settings.jwt_algorithm`
- секрет: `settings.secret_key`
- TTL: `settings.access_token_expire_minutes`

Проверка access token выполняется в `backend/app/core/dependencies.py` через `decode_token()` и затем через проверку `payload.token_type == TokenType.ACCESS`.

### JWT refresh token

Refresh token создаётся через `create_refresh_token()` и имеет те же базовые claims:

- `sub`
- `token_type=refresh`
- `iat`
- `exp`
- `jti`

TTL задаётся через `settings.refresh_token_expire_days`.

### Rotation и replay protection

Refresh-сессии защищаются через Redis-backed `TokenStore` в `backend/app/core/token_store.py`.

Используется две группы ключей:

- `token:allow:{jti}`
- `token:revoke:{jti}`

Текущая модель:

- при `register/login/oauth_login` новый refresh `jti` помещается в allow-list
- при `refresh` старый `jti` проверяется через `is_refresh_allowed()`
- затем старый `jti` revoke'ится
- после этого создаётся новая пара токенов
- новый refresh `jti` добавляется в allow-list

Это даёт базовую refresh rotation и блокировку повторного использования уже отозванного refresh token.

### Logout

`logout()` принимает refresh token, декодирует его и вызывает `revoke_refresh_jti()`.

Поведение:

- если токен отсутствует, logout возвращает success
- если токен невалиден, logout также возвращает success
- если Redis доступен, `jti` помечается revoked и удаляется из allow-list

Это соответствует идемпотентному logout API.

### Password hashing

Пароли обрабатываются через `passlib` + `bcrypt`:

- `hash_password()` -> `pwd_context.hash(...)`
- `verify_password()` -> `pwd_context.verify(...)`

Текущая схема:

- `bcrypt`
- `deprecated="auto"`

### Auth rate limiting

Auth endpoint'ы (`register/login/refresh/logout/oauth`) уже защищены limiter'ом через категорию `auth` в `backend/app/api/routes/v1/auth.py`.

Ключ строится по client IP:

- `auth_register:{host}`
- `auth_login:{host}`
- `auth_refresh:{host}`
- `auth_logout:{host}`
- `auth_oauth:{host}`

### Error envelope consistency

Auth path использует общий envelope и централизованные exception handlers:

- `401` для invalid token / invalid token type / inactive user / revoked refresh
- `409` для duplicate email
- `422` для validation paths
- `429` для auth rate limit
- `503` для session store unavailable

Формат ответа согласован:

- `ok`
- `message_key`
- `data`
- `error.code`
- `error.details`
- `meta`

## Что работает хорошо

### 1. Access и refresh токены разделены явно

В коде есть чёткое разделение через `token_type`, и access token нельзя использовать как refresh token, а refresh token нельзя использовать как bearer access credential.

### 2. Есть rotation и replay rejection

Модель allow/revoke по `jti` уже реализует базовую replay protection. Повторное использование refresh token после rotation приводит к `401 errors.auth.refresh_revoked`.

### 3. Redis failure для session store работает fail-closed

В отличие от rate limiter'а, session store для refresh-сессий не отключается silently. Если Redis недоступен:

- `register/login/oauth_login` не смогут выдать рабочую refresh session
- `refresh/logout` не смогут безопасно обновить/отозвать session state
- backend возвращает `503 errors.auth.session_store_unavailable`

С точки зрения session security это правильнее, чем fail-open.

### 4. Logout идемпотентен

Невалидный или отсутствующий refresh token не ломает logout endpoint и не раскрывает лишнюю информацию о состоянии сессии.

### 5. Password hashing присутствует и не хранит plain passwords

Local auth не сравнивает пароль напрямую и использует стандартную hash verify path.

## Основные риски и пробелы

### Critical: refresh rotation не атомарна

Текущий refresh flow в `AuthService.refresh()` делает последовательность:

1. `is_refresh_allowed(jti)`
2. `revoke_refresh_jti(jti)`
3. create new token pair
4. `allow_refresh_jti(new_jti)`

Это не атомарная Redis-операция. При конкурентных refresh-запросах с одним и тем же refresh token возможна race condition, где два запроса одновременно проходят шаг проверки до revoke.

Следствие:

- replay protection логически есть
- но при гонке она может быть обойдена
- для production-grade session rotation это главный security gap

### High: logout не проверяет token_type

`logout()` декодирует любой JWT и вызывает `_revoke_refresh(payload.jti)` без проверки `token_type == refresh`.

Практический эффект ограничен, потому что access token `jti` обычно не находится в allow-list refresh store, но поведение всё равно размытое:

- endpoint контрактно ожидает refresh token
- код принимает любой валидный JWT

Это не критическая уязвимость, но логически auth semantics здесь ослаблены.

### High: Redis является single point of session truth

Session security полностью зависит от Redis:

- allow-list refresh sessions
- replay protection
- revoke on logout

Если Redis недоступен, auth session flows начинают возвращать `503`. Это безопасно, но операционно рискованно: локальный outage Redis превращается в auth partial outage.

### High: OAuth login по-прежнему доверяет `id_token/code` как identity surrogate

`oauth_login()` фактически использует `payload.id_token or payload.code` как `provider_user_id` без реальной валидации у провайдера.

Следствие:

- можно создать или получить OAuth account path по произвольной строке
- это не проблема JWT-сессии как таковой, но это серьёзный auth integrity gap

Для production hardening это один из самых важных пробелов.

### Medium: access/refresh claims минимальны

Текущие claims включают только:

- `sub`
- `token_type`
- `iat`
- `exp`
- `jti`

Отсутствуют:

- `iss`
- `aud`
- `nbf`
- device/session binding metadata

Для внутреннего backend это допустимо, но production-grade token hygiene обычно требует хотя бы `iss` и `aud`.

### Medium: password hashing config не зафиксирована явно

Используется `bcrypt` через `passlib`, но:

- не задана явная cost policy
- не задана отдельная migration strategy beyond `deprecated="auto"`

Это не immediate bug, но делает security posture менее явной и менее контролируемой при future maintenance.

### Medium: нет session family / logout-all-sessions

Текущая модель ревокации работает на уровне отдельного refresh `jti`, но не даёт:

- session family tracking
- revoke all user sessions
- device-based session management

Для MVP это допустимо, для production user security - ограничение.

## Redis behavior summary

### Session store

Поведение при Redis проблемах:

- `allow_refresh_jti()` -> `RuntimeError("token_store_unavailable")`
- service layer маппит это в `503 errors.auth.session_store_unavailable`

Это fail-closed и с точки зрения security корректно.

### Rate limiting around auth

Auth rate limit использует Redis, но если limiter Redis-path недоступен, этот слой работает fail-open и только логирует `rate_limiter_degraded`.

Итог:

- session store -> fail-closed
- rate limiter -> fail-open

Такое смешанное поведение логически оправдано, но его нужно осознавать как часть threat model.

## Test coverage status

### Уже покрыто

Текущие тесты покрывают:

- payload validation для auth schemas
- access token decode path
- expired token rejection
- wrong token type rejection
- malformed access token rejection
- register/login/refresh/logout API envelope path
- replay rejection path
- inactive user rejection on login/refresh
- auth rate limit envelope consistency

### Не хватает тестов

Недостаточно или отсутствует покрытие для:

- Redis unavailable during `register/login/refresh/logout`
- atomicity/race condition around refresh rotation
- logout with access token instead of refresh token
- successful refresh integration path against real TokenStore/Redis
- OAuth security validation failure paths with real provider verification

## Итоговая оценка

Текущий auth/session слой можно оценить как `partially ready`.

Сильные стороны:

- корректная базовая JWT-модель
- access/refresh separation
- replay protection по `jti`
- fail-closed session store behavior
- согласованный error envelope
- рабочее покрытие основных негативных сценариев

Главные production gaps:

- неатомарная refresh rotation
- небезопасный OAuth identity flow
- отсутствие явной type-check логики в logout
- недостаточное покрытие Redis/session-store failure scenarios

## Recommended Next Task

Рекомендуемый следующий шаг: сделать refresh rotation атомарной в Redis одним compare-and-revoke/rotate operation path и добавить integration tests на concurrent refresh + Redis unavailable scenarios без изменения API-контракта.
