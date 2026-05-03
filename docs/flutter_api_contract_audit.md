# Flutter API Contract Audit

## 1. Executive Summary

Статус готовности backend API для Flutter-интеграции: **partially ready**.

Backend уже покрывает ключевые пользовательские потоки: auth, профиль, goals, uploads, meal analysis, reports, settings и localization. Ошибки возвращаются в единообразном envelope, JWT lifecycle стабилен, OpenAPI и Swagger доступны. Основной контрактный риск сейчас не в безопасности и не в runtime, а в полноте read-моделей для meal diary/detail flow: backend умеет создавать и анализировать приём пищи, но `MealDTO` недостаточно богат для мобильного клиента, который должен показывать nutrition summary, items и связанные изображения без догадок.

## 2. Verification Status

Проверено на текущем состоянии репозитория:

- `python -m pytest` -> `113 passed`
- `./scripts/check-backend.ps1` -> `passed`
- Внутри quality gate:
  - `alembic upgrade head` -> `ok`
  - `alembic current` -> `7bacdd57005a (head) (mergepoint)`
  - `python -m pytest` -> `113 passed`
  - optional health check -> `skipped`, backend отдельно не запускался на `127.0.0.1:8000`

## 3. What Is Ready For Flutter

### OpenAPI / docs

- Swagger UI доступен через `/docs`.
- OpenAPI schema доступна из стандартной FastAPI-конфигурации.
- Для Flutter это даёт discoverability по path/query/body параметрам.

Ограничение: значительная часть routes возвращает plain `dict` без явного `response_model`, поэтому OpenAPI хорошо описывает request side, но слабее описывает фактические response envelopes и вложенные `data` payloads.

### Auth and token lifecycle

Доступные endpoints:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `POST /api/v1/auth/oauth`

Готовность для Flutter:

- register/login возвращают пользователя и token pair
- refresh работает через rotation/replay protection
- logout стабилен
- OAuth для `google` и `apple` больше не принимает raw surrogate identity и требует provider verification

Вывод: стандартный mobile auth flow `login -> access token -> refresh -> logout` backend поддерживает без догадок.

### Profile / goals / onboarding

Доступные endpoints:

- `GET /api/v1/me`
- `PATCH /api/v1/me/profile`
- `PATCH /api/v1/me/locale`
- `GET /api/v1/goals/active`
- `POST /api/v1/goals`
- `PATCH /api/v1/goals/{goal_id}`

Готовность для Flutter:

- можно получить текущего пользователя и профиль
- можно завершить onboarding/profile setup
- можно создать и обновить активную цель
- enum-поля явно описаны backend-схемами

Вывод: onboarding и goals flow выглядят интеграционно готовыми.

### Uploads and meal analysis

Доступные endpoints:

- `POST /api/v1/uploads/init`
- `POST /api/v1/uploads/complete`
- `POST /api/v1/meals/analysis`

Готовность для Flutter:

- upload init возвращает `upload_id`, `storage_key`, `upload_url`, `upload_headers`, `expires_at`
- upload complete закрывает flow после прямой загрузки объекта в S3/MinIO
- meal analysis возвращает `items`, `estimated_nutrition`, `explanation`, `warnings`, `status`, `analyzed_at`

Вывод: фото-поток `init -> upload -> complete -> analysis` уже описан достаточно явно и не требует reverse engineering со стороны Flutter.

### Reports / settings / localization

Доступные endpoints:

- `GET /api/v1/reports/nutrition`
- `GET /api/v1/settings`
- `PATCH /api/v1/settings`
- `GET /api/v1/localization/locales`
- `POST /api/v1/localization/messages`

Готовность для Flutter:

- daily/period nutrition reporting уже возвращает агрегированные данные
- settings и locale/messages имеют понятные request/response формы
- localization API выглядит пригодным для remote message fetching

## 4. Contract Strengths

### Unified error envelope

Во всех проверенных модулях соблюдается единый contract:

- success:
  - `ok: true`
  - `message_key`
  - `data`
  - `error: null`
  - `meta`
- error:
  - `ok: false`
  - `message_key`
  - `data: null`
  - `error.code`
  - `error.details`
  - `meta`

Для Flutter это сильная сторона: можно централизовать обработку API errors без ветвления по endpoint.

### Stable auth/session behavior

- access и refresh token разделены корректно
- refresh rotation атомарна
- replay reuse даёт предсказуемый `401`
- Redis failure в session store fail-closed

Это важно для мобильного клиента, который зависит от предсказуемого refresh contract.

### Predictable formats

- `date` и `datetime` сериализуются как ISO-8601 через FastAPI/Pydantic
- enum-значения заданы backend-enum типами и выглядят стабильными

## 5. Contract Gaps And Flutter Guessing Points

### Meal read contract is under-specified

Ключевая проблема текущего контракта: `MealDTO` в read-path содержит только базовые поля:

- `id`
- `user_id`
- `title`
- `notes`
- `meal_type`
- `source`
- `eaten_at`
- `analysis_status`
- `created_at`
- `updated_at`

В нём нет:

- nutrition summary
- списка items
- связанных uploaded images
- breakdown, необходимого для diary/detail экранов

Следствие: Flutter не может надёжно построить полноценный meal history/detail UX только по backend response и будет вынужден либо хранить локальное промежуточное состояние, либо угадывать структуру из analysis response.

Это главный blocker для честной end-to-end contract readiness.

### OpenAPI is available but not strong enough for codegen-quality integration

Проблема не в отсутствии OpenAPI, а в том, что response side описан слабее, чем request side:

- многие endpoints не декларируют `response_model`
- envelope и вложенный payload часто формируются вручную
- pagination shape описана фактически, но не всегда формально как schema

Следствие: Flutter-команда может пользоваться `/docs`, но для строгой typed client generation этого недостаточно.

### Pagination is endpoint-specific, not standardized

На текущем backend pagination явно видна прежде всего в `GET /api/v1/meals`:

- `items`
- `total`
- `page`
- `page_size`

Контракт пригодный, но ad hoc. Единого стандартного paginated envelope для всех list endpoints сейчас нет.

### Numeric typing needs explicit client care

В нескольких доменных схемах используются `Decimal`.

Для Flutter это означает риск рассинхронизации, если клиент будет жёстко ожидать только `double` без tolerant parsing. Даже если текущая сериализация выглядит как JSON number, mobile DTO layer стоит проектировать осторожно.

### Analysis result and persisted meal are not yet the same read model

`POST /api/v1/meals/analysis` возвращает подробный analysis payload, но persisted `MealDTO` значительно беднее. Это создаёт разделение между:

- тем, что Flutter знает сразу после анализа
- тем, что Flutter сможет перечитать из backend позже

Для устойчивой mobile-интеграции эти два представления должны быть согласованы лучше, чем сейчас.

## 6. Endpoint-Level Readiness Assessment

### Ready

- `auth`
- `me`
- `goals`
- `uploads`
- `reports`
- `settings`
- `localization`

### Partially ready

- `meals`
- `meal analysis -> persisted meal readback`

Причина partial status: после успешного create/analyze Flutter не получает достаточно полного canonical meal representation для diary/detail read flows.

## 7. Can Flutter Implement Full App Flow Without Guessing?

### What can be implemented without guessing

- registration/login/logout/refresh
- profile setup
- locale/timezone update
- goals setup
- upload init/complete
- meal photo analysis screen
- reports screen
- settings/localization screens

### What still requires guessing or client-side workaround

- meal diary list with nutrition-rich cards
- meal detail screen with canonical backend data
- consistent re-fetch of analyzed meal after save

Итог: full app flow реализуем не полностью. Критический пробел находится в read-contract для meal entities.

## 8. Recommended Next Step

Следующий шаг: **выравнять meal read contract под потребности Flutter**.

Минимально необходимый scope:

- задать явные `response_model` для `GET /api/v1/meals` и `GET /api/v1/meals/{meal_id}`
- включить в canonical meal response:
  - nutrition summary
  - item list
  - uploaded image references
  - analysis-related fields, нужные для mobile detail/history
- зафиксировать это контрактными тестами, чтобы OpenAPI и реальный runtime больше не расходились

Пока этого нет, backend нельзя считать полностью готовым для Flutter-клиента без дополнительных предположений на стороне mobile app.
