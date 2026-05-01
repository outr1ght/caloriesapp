# Backend Audit Report

## 1. Executive Summary
Production readiness status: partially ready

Текущее состояние backend нельзя считать production-ready. Архитектурный каркас реализован: FastAPI, `/api/v1`, async SQLAlchemy, JWT, refresh token rotation/revoke через Redis, S3 upload abstraction, OpenAI wrapper, Celery skeleton, централизованный error envelope и Alembic. Однако production hardening блокируется проблемами runtime-окружения, несовпадением зависимостей для password hashing, ошибками в части тестов, нерабочим стандартным `python`/`pip` path и дефектом конфигурации Alembic (`alembic.ini` читается с BOM и ломает CLI). OpenAI-интеграция частично готова, но пока использует fallback/deterministic логику и не обеспечивает достаточный контроль стоимости или полноценную обработку vision payloads.

## 2. Project Structure
Ключевая структура backend подтверждена:

- Bootstrap: [backend/app/main.py](C:/Projects/caloriesapp/backend/app/main.py)
- Core: `backend/app/core/*`
- API: `backend/app/api/*`, versioned routes в `backend/app/api/routes/v1/*`
- DB: `backend/app/db/*`, ORM models в `backend/app/db/models/*`
- Services: `backend/app/services/*`
- Repositories: `backend/app/repositories/*`
- Integrations: `backend/app/integrations/*`
- Worker: `backend/app/worker/*`
- Tests: `backend/tests/*` (36 test files)
- Migrations: `backend/alembic/*`
- Config: `backend/pyproject.toml`, `backend/requirements.txt`, `backend/.env.example`

Отдельного каталога `backend/app/modules` нет.

Высокоуровневая схема слоёв:

- `app/main.py` инициализирует FastAPI, logging, CORS, lifespan и exception handlers.
- `api/routes/v1` содержит HTTP endpoints.
- `services` содержит прикладную бизнес-логику.
- `repositories` реализуют доступ к данным поверх async SQLAlchemy session.
- `integrations` инкапсулируют OpenAI, S3 и OAuth/barcode helpers.
- `worker` содержит Celery app и заглушечные background tasks.

## 3. What Works
Подтверждено по коду и/или runtime fallback-проверке:

- FastAPI приложение корректно инициализируется в [backend/app/main.py](C:/Projects/caloriesapp/backend/app/main.py).
- Версионирование API через `settings.api_v1_prefix`, по умолчанию `/api/v1`.
- Health-check endpoint реализован: `GET /api/v1/health` в `backend/app/api/routes/health.py`.
- Async DB слой реализован через `create_async_engine(...)` и `async_sessionmaker(...)` в `backend/app/core/database.py`.
- Repository layer присутствует, используется из service layer, базовый класс в `backend/app/repositories/base.py`.
- JWT auth реализован в `backend/app/core/security.py`; `get_current_user()` проверяет bearer token и тип access token.
- Refresh token flow реализован в `backend/app/services/auth_service.py` с Redis-backed allow/revoke через `backend/app/core/token_store.py`.
- Redis используется для rate limiting и refresh-token state.
- OpenAI wrapper использует `/v1/responses` и `response_format.type = json_schema`, что задаёт строгий JSON contract на уровне запроса.
- Есть fallback при отсутствии `APP_OPENAI_API_KEY` и retry loop в `OpenAIClient.generate_json()`.
- Upload/storage слой реализован через presigned S3 upload URL в `backend/app/integrations/storage_s3.py` и `backend/app/services/upload_service.py`.
- Централизованный error response реализован в `backend/app/common/exceptions.py` и `backend/app/common/responses.py`.
- JSON logging с маскированием чувствительных ключей реализован в `backend/app/core/logging.py`.
- При наличии рабочего интерпретатора backend фактически стартует и отвечает:
  - `/api/v1/health` вернул `{"ok":true,...}`
  - `/docs` вернул `HTTP/1.1 200 OK`

## 4. Critical Gaps
Blocking production issues:

- **Runtime environment not reproducible:** обязательные команды `python --version`, `pip list`, `python -m pytest`, `python -m uvicorn ...` в текущей среде не работают, так как `python` и `pip` отсутствуют в `PATH`. Это делает стандартный запуск backend неоперабельным.
- **Password hashing dependency mismatch:** код использует `CryptContext(schemes=["bcrypt"])` в `backend/app/core/security.py`, но установлен `passlib` без рабочего `bcrypt` backend. `pytest` подтверждает production-impacting failure: `passlib.exc.MissingBackendError: bcrypt: no backends available`.
- **Alembic CLI broken:** `python -m alembic heads` падает с `configparser.MissingSectionHeaderError` на `alembic.ini`, где первая строка читается как `'?[alembic]\n'`. В текущем состоянии migration CLI ненадёжен.
- **Refresh/auth critical tests failing:** test suite показывает реальные несовместимости между кодом и тестовыми ожиданиями для auth flow, в том числе 422 вместо ожидаемого 401 и жёсткая валидация `refresh_token` длины.
- **Async test infrastructure incomplete:** в `pyproject.toml` заявлен `pytest-asyncio`, но в установленном наборе зависимостей его нет; часть async tests пропускается и сопровождается `PytestUnknownMarkWarning` и `PytestUnhandledCoroutineWarning`, что снижает доверие к test suite.

## 5. High Priority Gaps
Must-fix before Flutter integration:

- **OAuth login is not production-safe:** `AuthService.oauth_login()` использует `id_token`/`code` фактически как `provider_user_id` без реальной верификации у Google/Apple.
- **OpenAI integration is only partially operational:** `MealAnalysisService` возвращает deterministic nutrition/items и использует OpenAI только для explanation/warnings, а не для полноценного анализа изображения. `image_ids` не используются для извлечения image content.
- **Cost control is weak:** есть только `model`, `timeout`, `retry count`; отсутствуют лимиты по токенам, budgeting, usage accounting, circuit breaker, request deduplication.
- **Rate limiting fails open:** при ошибках Redis в `enforce_user_rate_limit()` ограничение silently отключается.
- **Redis availability in lifespan is not enforced:** в `lifespan()` Redis `ping()` обёрнут в `try/except Exception: pass`, startup продолжится даже при неработающем Redis.
- **Celery layer is skeletal:** `meal_analysis_tasks.py` и `recommendation_tasks.py` содержат только заглушечные tasks, не связанные с реальным E2E flow.
- **Repository coverage is uneven:** есть базовый и специализированные repositories, но часть логики живёт напрямую в services без единообразного доменного контракта.
- **Test failures in contract/auth area:** backend уже не проходит полный `pytest`, значит интеграция с Flutter должна считаться нестабильной.

## 6. Medium Priority Gaps
Improvements:

- `backend/app/modules` отсутствует, хотя был ожидаем как часть структуры; это не runtime-блокер, но важно для унификации архитектурной документации.
- Logging JSON-форматтер редактирует только ключи заранее известного списка; request/response correlation, structured context enrichment, trace IDs и latency metrics не реализованы.
- `generic_exception_handler()` не логирует stack trace перед ответом 500.
- `OpenAIClient._parse_output()` полагается на сборку `output_text`; если OpenAI schema contract изменится, будет только soft fallback.
- `UploadService.complete_upload()` лишь проверяет наличие объекта в S3 и ставит `verified=True`; дополнительная антивирусная/metadata-проверка отсутствует.
- `S3StorageService` не реализует multipart upload, storage class policy, retry/backoff на стороне boto3 вызовов.
- `requirements.txt` и `pyproject.toml` расходятся по hashing stack: в одном `passlib[bcrypt]`, в другом `passlib[argon2]`.
- В каталоге backend появились временные `pytest-cache-files-*` директории с access issues, что указывает на неидеальную локальную test hygiene.

## 7. Test Status
Фактический результат запуска full suite через рабочий fallback interpreter:

```text
4 failed, 60 passed, 13 skipped, 34 warnings in 109.04s (0:01:49)
```

Основные падения:

- `tests/api/test_auth_flow.py::test_register_login_refresh_logout_flow`
  - `ValidationError` из `TokenPairDTO`: `refresh_token` короче 32 символов в тестовом мок-ответе.
- `tests/api/test_auth_flow.py::test_refresh_replay_rejected`
  - фактический статус `422`, ожидался `401`.
- `tests/api/test_meals_behavior.py::test_meal_not_found_and_ownership_errors`
  - `TypeError` из-за несовместимой monkeypatch-сигнатуры `_not_found()`.
- `tests/unit/test_auth_security.py::test_password_hash_roundtrip`
  - `passlib.exc.MissingBackendError: bcrypt: no backends available`.

Дополнительные замечания по test status:

- Async tests частично skipped из-за отсутствия подходящего pytest async plugin.
- Есть предупреждения `PytestUnknownMarkWarning` и `PytestUnhandledCoroutineWarning`.
- Есть `PytestCacheWarning` с ошибками создания `.pytest_cache` временных директорий.
- Покрытие по тематике присутствует: auth, meals, reports, uploads, OpenAI/AI, security, startup imports, storage resilience.

## 8. Runtime Status
### Required commands (exact commands requested)

```text
python --version
```

Result:

```text
python : Имя "python" не распознано как имя командлета, функции, файла сценария или выполняемой программы.
```

```text
pip list
```

Result:

```text
pip : Имя "pip" не распознано как имя командлета, функции, файла сценария или выполняемой программы.
```

```text
python -m pytest
```

Result:

```text
python : Имя "python" не распознано как имя командлета, функции, файла сценария или выполняемой программы.
```

```text
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Result:

```text
python : Имя "python" не распознано как имя командлета, функции, файла сценария или выполняемой программы.
```

Verification commands after failed startup:

```text
curl http://127.0.0.1:8000/api/v1/health
```

Result:

```text
curl : Невозможно соединиться с удаленным сервером
```

```text
curl http://127.0.0.1:8000/docs
```

Result:

```text
curl : Невозможно соединиться с удаленным сервером
```

### Fallback runtime check (non-standard, used only to separate code issues from PATH issues)

Через локальный portable interpreter backend стартует и отвечает:

- `GET /api/v1/health` -> `200 OK`, body:

```json
{"ok":true,"message_key":"messages.health.ok","data":{"status":"ok"},"error":null,"meta":{}}
```

- `HEAD /docs` -> `HTTP/1.1 200 OK`

Вывод: проблема стандартного runtime-check в первую очередь инфраструктурная (`python`/`pip` path), а не полный runtime crash приложения.

## 9. OpenAI Integration Status
Статус: partially ready

Что реализовано:

- Обёртка `OpenAIClient` в `backend/app/integrations/openai_client.py`.
- Используется endpoint `POST https://api.openai.com/v1/responses`.
- Передаётся `response_format.type = json_schema`.
- Есть retry loop на `TimeoutException`, `HTTPError`, `JSONDecodeError`, `ValueError`.
- Есть fallback при отсутствии API key: `openai_not_configured`.
- Есть fallback при исчерпании retry: `openai_unavailable`.
- Есть schema validation через Pydantic в `MealPhotoAnalyzer`.

Пробелы:

- Нет строгого контроля стоимости: отсутствуют `max_output_tokens`, budget guardrails, metering, per-user quotas.
- Нет streaming/cancellation strategy.
- Нет structured logging usage для AI calls.
- Нет real image-to-model payload в `MealAnalysisService`; фактический анализ изображения stubbed/deterministic.
- Нет отдельного circuit breaker или rate limit specifically for AI usage.

Итог: JSON contract и базовый retry/fallback присутствуют, production-grade AI pipeline пока не завершён.

## 10. Database / Redis / Migrations Status
### PostgreSQL / SQLAlchemy

- Async engine реализован корректно через `create_async_engine(...)`.
- `database_url` обязателен в settings.
- В `pyproject.toml` заявлен `asyncpg`, в runtime environment он установлен.
- Query layer строится вокруг `AsyncSession`, repositories и SQLAlchemy ORM.

### Redis

- Используется `redis.asyncio.Redis.from_url(...)`.
- Применяется для:
  - refresh token allow/revoke state
  - rate limiting
  - Celery broker/backend
- Startup не fail-fast при недоступности Redis.

### Alembic

- Миграции присутствуют: initial schema + language expansion + legacy compatibility revision.
- `alembic/env.py` использует async engine configuration и metadata из ORM.
- CLI-проверка `alembic heads` сейчас broken из-за `alembic.ini` parsing issue:

```text
configparser.MissingSectionHeaderError: File contains no section headers.
file: 'alembic.ini', line: 1
'?[alembic]\n'
```

- Дополнительный архитектурный риск: migration tree содержит `0001_initial.py` как legacy compatibility revision и требует отдельной верификации на linearity/heads после починки ini-файла.

## 11. Recommended Next Step
Устранить расхождение runtime/dependency bootstrapping для backend: привести к единому воспроизводимому Python environment с рабочими `python`/`pip` в `PATH`, исправить hashing backend (`bcrypt` vs installed packages) и восстановить полный green path для `python -m pytest` и `python -m uvicorn` как базу для дальнейшего production hardening.

