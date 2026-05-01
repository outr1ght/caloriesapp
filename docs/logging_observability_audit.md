# Logging & Observability Audit

## Контекст проверки

Проверка выполнена на локальном backend в состоянии:

- `python -m pytest` -> `77 passed`
- `./scripts/check-backend.ps1` -> `passed`
- `alembic current` -> `7bacdd57005a (head) (mergepoint)`

## Что уже есть

### 1. Базовая структурированная конфигурация логов

В [backend/app/core/logging.py](C:/Projects/caloriesapp/backend/app/core/logging.py) настроен JSON formatter для root logger через `logging.config.dictConfig(...)`.

Текущий формат включает:

- `level`
- `logger`
- `message`
- `module`
- `funcName`
- `lineNo`
- `time`

### 2. Базовое редактирование чувствительных ключей

В formatter есть маскирование по ключам:

- `password`
- `hashed_password`
- `token`
- `access_token`
- `refresh_token`
- `authorization`
- `secret`
- `api_key`

Это снижает риск прямой утечки секретов в structured payload, если словарь будет передан в лог.

### 3. Единый error contract для API

В [backend/app/common/exceptions.py](C:/Projects/caloriesapp/backend/app/common/exceptions.py) все `AppException`, validation errors и generic exceptions преобразуются в единый JSON envelope через `error_response(...)`.

Это хорошо для API-consistency, но это не равно observability: сами ошибки почти не логируются.

## Основные наблюдения

### A. Startup / shutdown observability слабая

В [backend/app/main.py](C:/Projects/caloriesapp/backend/app/main.py):

- `configure_logging()` вызывается при старте
- `lifespan()` делает `redis_client.ping()`
- исключение в `ping()` подавляется через `except Exception: pass`
- явных startup/shutdown логов нет

Следствие:

- нет события «application started»
- нет события «redis unavailable on startup»
- нет события «application shutdown complete»

### B. Request logging отсутствует

В кодовой базе нет request/response middleware для access logging.

Сейчас нет стандартных production-событий:

- method
- path
- status_code
- duration_ms
- request_id
- user_id
- client_ip

В результате расследование инцидентов по конкретному запросу затруднено.

### C. Exception handlers возвращают корректный API-ответ, но не пишут лог

В [backend/app/common/exceptions.py](C:/Projects/caloriesapp/backend/app/common/exceptions.py):

- `app_exception_handler(...)` не логирует бизнес-ошибки
- `validation_exception_handler(...)` не логирует invalid request
- `generic_exception_handler(...)` не логирует stack trace unexpected error

Следствие:

- 500-ошибки не оставляют server-side trace в коде приложения
- 4xx security/validation события невидимы для ops/forensics

### D. Auth / security observability слабая

В [backend/app/core/dependencies.py](C:/Projects/caloriesapp/backend/app/core/dependencies.py) и [backend/app/services/auth_service.py](C:/Projects/caloriesapp/backend/app/services/auth_service.py):

- invalid token
- wrong token type
- revoked refresh token
- inactive account
- user not found
- session store unavailable

все эти состояния корректно превращаются в `AppException`, но не логируются.

Следствие:

- нет аудита auth failures
- нет видимости по replay/revoke событиям refresh token
- нет агрегируемой картины security incidents

Плюс: сами токены в логах сейчас не печатаются, что правильно.

### E. Redis / rate limit проблемы частично скрываются

В [backend/app/core/rate_limit.py](C:/Projects/caloriesapp/backend/app/core/rate_limit.py):

- при `RedisError` rate limiting quietly disables itself через `return`
- логов о деградации нет

В [backend/app/core/token_store.py](C:/Projects/caloriesapp/backend/app/core/token_store.py):

- Redis ошибки превращаются в `RuntimeError("token_store_unavailable")`
- далее они поднимаются как `503`
- но источник ошибки и контекст не логируются

Следствие:

- для rate limiting возможен silent degradation
- для session store outage клиент видит 503, но оператор не получает полезного structured event

### F. DB failure visibility ограничена

В [backend/app/core/database.py](C:/Projects/caloriesapp/backend/app/core/database.py):

- engine создаётся без явных логов о connect/init
- session lifecycle не логируется
- SQLAlchemy exception paths не оборачиваются application-level logging

Сейчас DB-проблемы видны в traceback процесса, но не оформлены как предсказуемые structured operational events.

### G. OpenAI integration почти непрозрачна

В [backend/app/integrations/openai_client.py](C:/Projects/caloriesapp/backend/app/integrations/openai_client.py):

- есть retry loop
- есть fallback response (`openai_not_configured`, `openai_unavailable`, `empty_openai_output`)
- но отсутствуют логи:
  - attempt number
  - timeout
  - HTTP error class/status
  - fallback activation
  - response parse failure

Плюс:

- API key не логируется
- prompt/body целиком не логируются, что безопаснее с точки зрения privacy

Минус:

- невозможно понять, почему AI path degraded в production
- нет cost/usage observability вообще

### H. Upload / storage observability слабая

В [backend/app/services/upload_service.py](C:/Projects/caloriesapp/backend/app/services/upload_service.py) и [backend/app/integrations/storage_s3.py](C:/Projects/caloriesapp/backend/app/integrations/storage_s3.py):

- ошибки S3/MinIO поднимаются корректно как `503`
- но нет логов для:
  - `create_presigned_upload` failure
  - `head_object` failure
  - upload verification mismatch / missing object

Следствие:

- storage outage виден клиенту, но не даёт операционного следа на backend-стороне

### I. OAuth external provider visibility слабая

В [backend/app/integrations/oauth/google.py](C:/Projects/caloriesapp/backend/app/integrations/oauth/google.py) и [backend/app/integrations/oauth/apple.py](C:/Projects/caloriesapp/backend/app/integrations/oauth/apple.py):

- provider verification failures преобразуются в 401/422
- external call/claim parsing не логируются

Следствие:

- невозможно отличить массовую ошибку провайдера от пользовательских invalid tokens

## Риски по секретам и PII

### Что выглядит приемлемо

- access/refresh token не логируются напрямую
- password / hashed password маскируются formatter'ом
- OpenAI API key не печатается в коде

### Что остаётся рискованным

- formatter маскирует только ключи в `dict`, но почти нигде не используются structured extra-payload логи, поэтому защита сейчас мало проверена в реальном runtime
- synthetic OAuth email и user email потенциально могут попасть в будущие message strings, если начать логировать без нормализации
- validation error details могут содержать пользовательский ввод; если логировать их как есть, нужен deliberate redaction policy

## Оценка production-readiness observability

### Плюсы

- есть JSON logging foundation
- есть единый error envelope
- нет очевидной текущей утечки секретов в логах
- health endpoint и quality gate существуют

### Минусы

- почти нет собственно application logs
- нет access logs / request correlation
- нет exception stack traces на уровне handlers
- нет явной видимости по DB/Redis/OpenAI/S3 degradation
- нет security-event trail для auth failures

## Короткий план улучшений

### Приоритет 1

Добавить request/response middleware и request correlation:

- `request_id`
- method/path/status
- duration
- optional `user_id`

### Приоритет 2

Начать логировать все exception handler paths:

- `AppException` как warning/info по классу ошибки
- validation failures как warning
- unexpected exceptions как error + traceback

### Приоритет 3

Добавить structured logs в operational integrations:

- Redis/rate-limit degradation
- token store failures
- OpenAI retry/fallback paths
- S3/MinIO failures
- startup/shutdown milestones

## Рекомендуемая следующая задача

**Добавить request correlation + centralized request/error logging middleware для FastAPI**

Почему именно это:

- это даёт максимальный прирост observability без изменения API-контракта
- это создаёт основу для последующих auth/DB/OpenAI/S3 логов
- это улучшит разбор production incidents быстрее, чем точечное логирование по отдельным сервисам
