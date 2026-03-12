# Mobile Architecture

## Layers
- Presentation: screens, widgets, Riverpod state notifiers.
- Application: use cases (analyze photo, save meal, generate report).
- Domain: entities and repository interfaces.
- Data: Dio API clients, DTO mappers, local cache.

## Routing
`go_router` with guarded routes:
- unauthenticated: splash, onboarding, auth
- authenticated: dashboard, capture, diary, reports, settings

## State Handling
- AsyncValue for loading/error/data.
- Optimistic UI for meal save and weight log add.
- Centralized app error mapper for user-safe messages.

## Localization
ARB resources in `/mobile_app/lib/l10n` for EN/ES/DE/FR/RU.
