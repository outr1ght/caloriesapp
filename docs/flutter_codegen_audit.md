# Flutter Codegen Audit

## 1. Executive Summary

Статус готовности Flutter workspace к API client generation: **partially ready**.

Backend теперь публикует воспроизводимый OpenAPI artifact в `docs/openapi/openapi.json`, а mobile-приложение уже имеет выраженный data/domain/application/presentation split. Это делает codegen целесообразным, но не как прямую замену всего networking слоя. Текущий Flutter client построен вокруг hand-written `Dio` wrapper, raw `Map<String, dynamic>` datasources, ручных DTO и repository-to-domain мапперов. Поэтому лучший путь не "сгенерировать всё и заменить всё", а добавить generated transport layer под существующие repositories.

## 2. Workspace State

### Project structure

В `mobile_app/lib` уже есть стабильная архитектура:

- `core`
  - config
  - error
  - network
  - storage
- `data`
  - `datasources`
  - `models`
  - `repositories`
- `domain`
  - `entities`
  - `repositories`
- `application`
  - providers
  - usecases
- `presentation`
  - features
  - router
  - theme
  - widgets

Это хороший признак для codegen integration: generated API client можно ограничить data-layer и не тащить его в UI/application напрямую.

### Existing networking/auth setup

Текущий networking stack:

- `dio` уже используется как основной HTTP client
- `ApiClient` обрабатывает refresh-on-401
- `TokenStorage` хранит `access/refresh` в `flutter_secure_storage`
- `dio_client.dart` уже мапит backend error envelope в `AppError`

Вывод: transport codegen должен работать поверх `Dio`, а не тащить новый HTTP stack.

### Existing DTO/data mapping style

Сейчас datasources возвращают в основном `Map<String, dynamic>`, а repositories делают manual parsing:

- `MealsApiDatasource` -> raw map
- `MealRepositoryImpl` -> `MealModel.fromJson`
- `ReportsApiDatasource` -> raw map
- `NutritionReportModel.fromApi`
- `AuthApiDatasource` -> partial envelope parsing вручную

Это даёт control, но уже ведёт к drift между backend и mobile contract.

## 3. Verified Tooling Status

Проверка CLI в текущем окружении:

- `flutter --version` -> failed
- `flutter pub get` -> failed
- `flutter test` -> failed

Фактическая ошибка во всех случаях:

```text
flutter : The term 'flutter' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

Следствие: readiness audit можно сделать по коду, но не по живой Flutter build/test verification на этой машине.

## 4. Key Findings

### 4.1 Current client is not generator-driven

В `pubspec.yaml` нет признаков generator-centric stack:

- нет `retrofit`
- нет `json_serializable`
- нет `freezed`
- нет `build_runner`
- нет `chopper`

Это означает, что `retrofit.dart` и `chopper` потребуют дополнительной инфраструктуры генерации и заметной перестройки существующего data layer.

### 4.2 Existing manual DTOs already drift from backend contract

Наиболее показательный пример: meals.

Backend теперь возвращает canonical meal read contract с:

- `eaten_at`
- `nutrition_summary`
- `items`
- `images`
- pagination через `data.items + data.meta`

Но `mobile_app/lib/data/models/meal_models.dart` всё ещё ожидает:

- `nutrition.calories`
- fallback на `logged_at`
- сильно урезанную meal-модель

Дополнительно `mobile_app/test/data/meals_repository_test.dart` использует payload:

- `logged_at`
- `nutrition.calories`

который уже не совпадает с backend contract.

Это сильный аргумент в пользу generated transport DTO layer: текущий ручной mapping уже начал расходиться с источником истины.

### 4.3 Existing repository/provider architecture should be preserved

Текущая архитектура уже отделяет:

- API access
- repository orchestration
- domain entities
- Riverpod state
- routing/localization/UI

Это важно: generated code не должен напрямую проникать в `application`/`presentation`.

Лучший integration boundary:

- generated client + generated DTOs в data/remote layer
- hand-written adapters -> domain entities
- текущие repositories/providers остаются orchestration layer

### 4.4 Auth integration already has custom behavior that should not be overwritten

`ApiClient` сейчас умеет:

- хранить bearer header
- делать refresh-on-401
- очищать session при refresh failure
- не refresh-ить auth endpoints

Если codegen заменить этим прямой generated client без adapter/interceptor integration, легко потерять текущую session semantics.

### 4.5 Error handling is already opinionated and should be reused

`dio_client.dart` мапит backend envelope в `AppError(message, code, statusCode)`.

Это означает, что generated transport layer должен:

- либо использовать тот же `Dio` instance
- либо быть обёрнут thin adapter-слоем, который конвертирует transport exceptions в текущий `AppError`

Иначе app получит второй параллельный способ обработки ошибок.

### 4.6 App config still has environment fragility

`app_config.dart` по-прежнему имеет fallback:

- Android: `http://10.0.2.2:8000/api/v1`
- non-Android: `http://192.168.0.108:8000/api/v1`

Это machine-specific и не связано напрямую с codegen, но для generated client consumption это всё ещё runtime risk.

## 5. Best-Fit Codegen Approach

### Recommended approach: OpenAPI Generator -> Dio transport layer only

Лучший fit для текущего workspace: **OpenAPI Generator с Dart/Dio client generation**, но только как generated transport layer.

Почему именно это:

- backend уже публикует canonical OpenAPI artifact
- mobile уже использует `dio`
- не требуется переписывать providers/usecases/router
- можно генерировать клиента из backend schema, а не поддерживать второй набор annotations в Flutter codebase
- generated DTOs помогут убрать raw-map parsing drift

### Why not retrofit.dart

`retrofit.dart` плохо подходит как основной путь здесь, потому что:

- потребует вручную поддерживать annotated API interfaces в Flutter
- OpenAPI schema тогда перестанет быть главным source of truth
- нужны `retrofit`, `build_runner`, `json_serializable`
- это ближе к частичному переписыванию существующего datasource layer, чем к чистой интеграции

### Why not chopper

`chopper` тоже менее удачен:

- в проекте уже есть `dio`
- придётся тянуть второй transport idiom
- выигрыш по сравнению с generated OpenAPI client невысок

### Why not continue manual DTO mapping only

Manual mapping уже начал расходиться с backend contract. После последних backend-hardening шагов эта проблема будет только расти.

## 6. Recommended Placement For Generated Code

Лучшее размещение generated code:

- `mobile_app/lib/data/generated/openapi/`

или, если команда хочет более жёсткую изоляцию:

- `mobile_app/lib/data/remote/generated/openapi/`

Что не стоит делать:

- не генерировать в `domain/`
- не генерировать в `presentation/`
- не смешивать generated DTOs с hand-written domain entities
- не генерировать поверх существующих `data/models/*.dart`

## 7. Integration Strategy Without Overwriting Hand-Written Models

Рекомендуемый слой ответственности:

1. Generated OpenAPI client
- знает только transport DTOs и endpoint calls

2. Hand-written datasource adapter
- вызывает generated API methods
- unwrap-ит envelope при необходимости
- переводит generated DTOs в существующие repository-facing models или сразу в domain mappers

3. Existing repositories
- остаются boundary между data и domain
- продолжают возвращать `MealEntity`, `UserSession`, `NutritionReportEntity` и т.д.

4. Existing providers/usecases
- не зависят от codegen напрямую

Это минимизирует риск массовой перетряски приложения.

## 8. Concrete Risks To Address Before Codegen Rollout

### Contract drift in current tests

Есть тесты, уже использующие устаревшие payload assumptions, особенно для meals. Их нужно поправить до или одновременно с migration на generated transport DTOs.

### Envelope handling

Backend везде использует `ok/message_key/data/error/meta`. Flutter codegen не должен наивно ожидать, что endpoint response сразу равен payload. Понадобится либо:

- generic envelope wrappers
- либо thin datasource adapters, которые извлекают `data`

### Pagination wrappers

После стандартизации backend list endpoints теперь используют:

- `data.items`
- `data.meta`

Generated models должны учитывать именно эту структуру, а не старый flat `total/page/page_size`.

### Auth/session refresh coupling

Generated client нельзя внедрять в обход текущего `ApiClient`/auth flow. Иначе можно сломать:

- bearer injection
- refresh retry
- logout/session clear behavior

## 9. Recommended Next Step

Следующий шаг: **внедрить proof-of-concept generated transport layer только для `auth + meals`**.

Минимальный безопасный scope:

- генерировать OpenAPI client из `docs/openapi/openapi.json`
- положить generated код в отдельную `data/generated/openapi` папку
- подключить generated `auth` и `meals` endpoints через thin datasource adapters
- не трогать domain entities, providers и UI
- обновить mobile tests, чтобы они использовали новый canonical backend contract

Это даст быстрый сигнал, насколько cleanly codegen вписывается в текущую архитектуру, не превращая миграцию в большой bang rewrite.

## 10. Implementation Update

В репозитории внедрён initial OpenAPI-driven generated transport layer:

- generator script: `scripts/generate-flutter-api-client.ps1`
- generated output: `mobile_app/lib/data/api/generated/`
- current integration scope: `auth + meals`
- integration mode: generated transport DTO/API -> hand-written datasource/repository mapping -> existing domain entities/providers
