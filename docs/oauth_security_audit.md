# OAuth Security Audit

## Контекст проверки

В рамках аудита выполнены:

- `python -m pytest` -> `104 passed`
- `./scripts/check-backend.ps1` -> `passed`

Это подтверждает, что выводы ниже относятся к текущему рабочему состоянию backend.

## Поддерживаемые провайдеры

На уровне enum в `backend/app/db/models/enums.py` объявлены:

- `local`
- `google`
- `apple`

Других OAuth-провайдеров в кодовой базе не обнаружено.

## Реальный runtime flow `oauth_login()`

Текущий основной flow расположен в `backend/app/services/auth_service.py`.

Фактическое поведение:

1. `provider=local` отвергается с `422 errors.auth.invalid_oauth_provider`
2. `provider_user_id = payload.id_token or payload.code`
3. если ни `id_token`, ни `code` нет -> `422 errors.auth.oauth_missing_token`
4. backend ищет identity по паре:
   - `provider`
   - `provider_user_id`
5. если identity уже существует -> логинит связанного пользователя
6. если identity нет -> создаёт нового пользователя с synthetic email:
   - `{provider}_{provider_user_id[:16]}@oauth.local`
7. далее выдаёт обычную локальную JWT session pair

Ключевой факт:

- текущий runtime path не вызывает provider-specific verification layer
- `id_token` или `code` используются как surrogate identity string
- никакой криптографической или протокольной проверки провайдера в этом path нет

С точки зрения security это главный риск всей OAuth-реализации.

## Provider helpers: что есть в коде

### Apple helper

В `backend/app/integrations/oauth/apple.py` есть `AppleOAuthProvider.resolve_user()`.

Что он делает:

- требует `id_token`
- пытается распарсить JWT локально
- извлекает `sub`, `email`, `email_verified`

Но при этом:

- `verify_signature = False`
- `verify_exp = False`
- `verify_nbf = False`
- `verify_iat = False`
- `verify_aud = False`
- `verify_iss = False`

Итог:

- helper не проверяет подпись Apple
- не проверяет issuer
- не проверяет audience/client id
- не проверяет expiration
- не проверяет nonce

Даже если бы этот helper использовался в runtime, в текущем виде он небезопасен для production.

### Google helper

В `backend/app/integrations/oauth/google.py` есть `GoogleOAuthProvider.resolve_user()`.

Что он делает:

- требует `id_token`
- отправляет его в `https://oauth2.googleapis.com/tokeninfo`
- при `200` возвращает `sub`, `email`, `email_verified`, `name`

Плюсы:

- есть удалённая валидация токена через Google endpoint
- helper извлекает реальные provider claims

Пробелы:

- helper не используется в текущем `AuthService.oauth_login()` path
- нет явной проверки against configured client `aud`
- нет nonce/state handling
- нет account-linking policy beyond `provider + provider_user_id`

## Что не реализовано в текущем runtime path

### 1. Нет реальной валидации `id_token` или `code`

Backend не делает:

- token exchange по OAuth authorization code
- verification of issuer
- verification of audience / client id
- verification of token expiration
- verification of signature/JWKS
- nonce verification
- state verification

Иными словами, любой произвольный `id_token` или `code`-like string может стать `provider_user_id`.

### 2. Нет JWKS/signature verification

В рабочем `oauth_login()` вообще нет JWKS path.

В Apple helper signature verification explicitly disabled.

### 3. Нет issuer / audience / expiration checks

Для рабочего runtime path их нет вовсе.

Для Apple helper они тоже отключены.

Для Google helper часть проверки косвенно делегирована `tokeninfo`, но helper не используется в auth service.

### 4. Нет nonce/state handling

В кодовой базе не найдено runtime-механизма для:

- сохранения/проверки `state`
- генерации/проверки `nonce`

Это означает, что стандартные protections against CSRF/replay in OAuth authorization flow сейчас отсутствуют.

## Account linking behavior

Текущая логика identity lookup:

- lookup only by `provider + provider_user_id`

Если identity не найдена:

- создаётся новый user
- synthetic email строится из provider string/token prefix
- email linking к существующему local account не выполняется
- merge policy отсутствует

Риски:

- нельзя безопасно связать local и OAuth account по verified email
- возможно создание лишних/дублирующих user records
- synthetic email не подтверждает владение реальным email identity

С точки зрения безопасности важнее другое: так как `provider_user_id` сейчас не верифицируется, attacker может инициировать создание предсказуемых OAuth-shaped identities.

## Error envelope consistency

OAuth endpoint использует тот же стандартный error envelope, что и остальной auth layer.

Observed contracts:

- `422 errors.auth.invalid_oauth_provider`
- `422 errors.auth.oauth_missing_token`
- `401 errors.auth.oauth_invalid_token` в helper’ах
- `503 errors.auth.session_store_unavailable` на выдаче refresh session при Redis problem

С точки зрения API consistency здесь всё хорошо. Проблема не в envelope, а в отсутствии настоящей provider verification.

## Tests coverage

Что видно по текущим тестам:

- прямого покрытия valid/invalid OAuth provider token flows практически нет
- есть только косвенное покрытие schema validation и базовых auth paths
- нет integration/unit tests на:
  - valid Google token
  - invalid Google token
  - valid Apple token
  - malformed Apple token
  - issuer/audience mismatch
  - expired provider token
  - missing/invalid nonce/state
  - account linking decisions

Итог:

- самый рискованный auth path сейчас почти не защищён тестами

## Итоговая оценка

Текущий OAuth login слой можно оценить как `not production ready`.

Почему:

- основной `oauth_login()` не делает реальной provider verification
- Apple helper даже в изоляции отключает все важные JWT checks
- Google helper выглядит лучше, но не встроен в runtime auth path
- нет nonce/state handling
- нет verified account linking policy
- нет meaningful test coverage на security-critical OAuth flows

## Recommended Next Task

Рекомендуемый следующий шаг: заменить surrogate `id_token/code` flow на реальную provider-specific verification в `AuthService.oauth_login()` с обязательными checks `issuer/audience/expiration/signature`, а для authorization-code paths добавить `state/nonce` handling и security tests без изменения API envelope.
