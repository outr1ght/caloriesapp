# Backend Architecture

## Module Map
- `app/api/v1/endpoints`: HTTP transport layer only.
- `app/services`: domain orchestration and policies.
- `app/db/repositories`: persistence access.
- `app/schemas`: request/response DTO contracts.
- `app/core`: config, auth, localization, logging, errors.

## Patterns
- API version prefix: `/api/v1`.
- SQLAlchemy session per request.
- Repository + service layering.
- Pydantic validation at API boundary.
- Key-based localized errors (`error.code`, `error.message`).

## Background Jobs
Celery selected over RQ because:
- better mature retry semantics
- task routing and scheduling capabilities
- stronger ecosystem for production workloads

## Security Defaults
- JWT access + refresh rotation
- password hashing with Argon2
- upload validation and size caps
- input sanitization and AI output schema validation
