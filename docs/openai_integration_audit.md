# OpenAI Integration Audit

## Контекст проверки

Проверка выполнена на локальном backend в состоянии:

- `python -m pytest` -> `78 passed`
- `./scripts/check-backend.ps1` -> `passed`
- request/error logging уже добавлены

## Что сейчас реализовано

### 1. Инициализация клиента

В [backend/app/integrations/openai_client.py](C:/Projects/caloriesapp/backend/app/integrations/openai_client.py):

- `OpenAIClient` читает настройки через `get_settings()`
- base URL захардкожен как `https://api.openai.com/v1`
- используются настройки:
  - `APP_OPENAI_API_KEY`
  - `APP_OPENAI_MODEL`
  - `APP_OPENAI_TIMEOUT_SECONDS`
  - `APP_OPENAI_MAX_RETRIES`

### 2. Использование в meal analysis

В [backend/app/services/meal_analysis_service.py](C:/Projects/caloriesapp/backend/app/services/meal_analysis_service.py):

- endpoint `POST /api/v1/meals/analysis` вызывает `MealAnalysisService.analyze(...)`
- основная nutrition-оценка сейчас deterministic stub
- OpenAI используется только для генерации `explanation` и `warnings`
- если OpenAI недоступен, explanation/warnings деградируют к локальному fallback

Следствие:

- текущий AI path не является критическим для calories/macros
- user-facing nutrition сейчас не зависит от реального vision/model inference

### 3. JSON response format от OpenAI

`OpenAIClient.generate_json(...)` отправляет `response_format.type = json_schema` и передаёт schema в API payload.

Это хороший базовый шаг к strict JSON output.

## Основные наблюдения

### A. Строгий JSON contract неполный

Хотя клиент просит `json_schema`, в [backend/app/integrations/openai_client.py](C:/Projects/caloriesapp/backend/app/integrations/openai_client.py):

- не проверяется, что OpenAI действительно вернул schema-conformant объект
- `_parse_output(...)` гарантирует только то, что output можно распарсить в `dict`
- сам `MealAnalysisService` не валидирует AI payload через отдельную Pydantic-схему

В `meal_analysis_service.py` после вызова клиента берутся:

- `ai.get("explanation")`
- `ai.get("warnings", [])`

Если schema нарушена, path не падает, а silently деградирует к строке/default list.

Итог:

- strict JSON contract реализован на transport/request уровне, но не на domain-validation уровне

### B. Schema validation присутствует не в основном meal-analysis path, а в соседних интеграциях

Есть более строгие consumer paths:

- [backend/app/integrations/meal_photo_analyzer.py](C:/Projects/caloriesapp/backend/app/integrations/meal_photo_analyzer.py)
- [backend/app/integrations/recommendation_generator.py](C:/Projects/caloriesapp/backend/app/integrations/recommendation_generator.py)

Там raw OpenAI output проходит через Pydantic validation и при mismatch превращается в `AppException(... invalid_ai_output ...)`.

Но текущий основной route `/api/v1/meals/analysis` этим путём не пользуется.

Итог:

- в кодовой базе есть паттерн правильной schema validation
- но production meal-analysis endpoint пока использует более слабый вариант

### C. Retry behavior базовый, но грубый

В `OpenAIClient.generate_json(...)`:

- retry count = `max(openai_max_retries, 0)`
- retry loop без backoff/jitter
- retry выполняется на:
  - `httpx.TimeoutException`
  - `httpx.HTTPError`
  - `json.JSONDecodeError`
  - `ValueError`

Проблемы:

- нет различения retryable и non-retryable HTTP statuses
- 4xx тоже попадают под `HTTPError` и будут ретраиться
- нет exponential backoff
- нет circuit breaking или request budget

### D. Timeout handling есть, но только на client level

- используется `httpx.AsyncClient(timeout=settings.openai_timeout_seconds)`
- timeout корректно попадает в retry/fallback path

Ограничение:

- нет отдельного connect/read/write timeout split
- нет внешнего cancellation budget на business-operation уровне

### E. Fallback behavior безопасный, но слишком тихий

Если API key не задан:

- возвращается `{"text": "", "items": [], "warnings": ["openai_not_configured"]}`

Если retries исчерпаны:

- возвращается `{"text": "", "items": [], "warnings": ["openai_unavailable"]}`

Если output пустой:

- `_parse_output(...)` возвращает `{"text": "", "items": [], "warnings": ["empty_openai_output"]}`

Это хорошо тем, что:

- endpoint не падает
- секреты не утекают
- UX может деградировать мягко

Но плохо тем, что:

- оператор не получает server-side diagnostic event
- нет различения timeout / 401 / 429 / 500 / malformed JSON на observability уровне

### F. Cost controls ограничены

Сейчас реально есть только:

- выбор модели через `APP_OPENAI_MODEL`
- timeout
- retry count
- upload size limit на backend уровне: `APP_MAX_UPLOAD_BYTES=5242880`

Но для OpenAI path отсутствуют:

- token budget / `max_output_tokens`
- явное ограничение prompt size
- image token budgeting
- dynamic model tiering
- cost/usage telemetry
- rate limiting specifically for AI-heavy endpoints beyond generic per-minute limiter

Важно:

- текущий `MealAnalysisService` вообще не отправляет изображения в OpenAI
- значит image-size limit пока влияет на uploads, но не контролирует фактический OpenAI spend

### G. Error mapping в API частично обходится fallback'ом

Для route `/api/v1/meals/analysis`:

- отсутствующие изображения -> `422 errors.analysis.missing_images`
- invalid UUID -> `422`
- OpenAI network/parse/provider problems чаще не превращаются в API error envelope, а гасятся fallback response внутри `OpenAIClient`

Итог:

- endpoint стабилен
- но клиент не отличает «AI реально сработал» от «мы показали fallback rationale» кроме warnings list

### H. Logging по OpenAI path недостаточное

С учётом текущих logging improvements, в OpenAI path всё ещё нет structured logs на:

- start/end of OpenAI request
- attempt number
- model name
- timeout/failure class
- fallback activation
- malformed JSON/schema mismatch

Плюсы:

- API key не логируется
- prompt/body сейчас не логируются, это снижает риск утечки PII

Минусы:

- operational debugging остаётся слабым
- нельзя безопасно отличить infra issue от provider rejection

### I. PII / secrecy posture сейчас относительно безопасный

В текущем коде:

- `Authorization` header с bearer key не логируется
- OpenAI API key формируется только в headers внутри клиента
- request/response bodies OpenAI не логируются
- image payload напрямую не передаётся в OpenAI path текущего meal analysis

Риск остаётся в будущем, если начнут логировать prompts без redaction policy.

## Тестовое покрытие

### Что покрыто

В [backend/tests/unit/test_openai_client_resilience.py](C:/Projects/caloriesapp/backend/tests/unit/test_openai_client_resilience.py):

- `openai_api_key is None` -> `openai_not_configured`
- empty parsed output -> `empty_openai_output`

В [backend/tests/test_meal_analysis_service.py](C:/Projects/caloriesapp/backend/tests/test_meal_analysis_service.py):

- отсутствие image ids -> `AppException`

В [backend/tests/api/test_meal_analysis_behavior.py](C:/Projects/caloriesapp/backend/tests/api/test_meal_analysis_behavior.py):

- success path маршрута
- invalid UUID
- service error path

### Что не покрыто

- retry on timeout / HTTP errors
- exhausted retries -> `openai_unavailable`
- malformed JSON from model
- non-dict parsed JSON
- schema mismatch for AI explanation/warnings payload
- real propagation of warnings from OpenAI fallback to `/meals/analysis`
- logging assertions for AI failures
- model/settings usage assertions

Итог:

- coverage для resilience path есть только в минимальном объёме
- основная operational failure matrix не покрыта

## Оценка текущего состояния

### Сильные стороны

- OpenAI integration optional и не ломает meal analysis endpoint
- есть configurable model/timeout/retry knobs
- есть request-side JSON schema format
- нет явной утечки API key в логах
- deterministic nutrition делает endpoint стабильнее

### Слабые стороны

- основной `/meals/analysis` path не валидирует AI output строгой Pydantic-схемой
- retries не различают retryable/non-retryable provider errors
- отсутствуют cost/usage controls и telemetry
- fallback path слишком тихий для production operations
- AI фактически не анализирует изображения, а только пишет explanation/warnings к deterministic estimate

## Рекомендуемая следующая задача

**Усилить `OpenAIClient` и `MealAnalysisService` строгой schema validation + structured fallback logging**

Минимальный безопасный объём следующего шага:

- ввести Pydantic validation для AI output в основном meal analysis path
- логировать timeout / HTTP error / fallback activation без утечки prompt/API key
- не менять response envelope и не делать OpenAI hard dependency

Это даст максимальный выигрыш по надёжности и observability без изменения внешнего API-контракта.
