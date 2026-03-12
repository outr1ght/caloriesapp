# System Architecture

## Context
- Mobile client calls FastAPI via JWT auth.
- FastAPI persists transactional data in PostgreSQL.
- Redis backs Celery queues, caching, and rate limiting.
- S3 stores uploaded meal images.
- AI pipeline orchestrated in backend service layer, with optional external model services.

## Data Flow (photo meal)
1. User uploads image from mobile.
2. Backend validates MIME/size and stores object in S3.
3. Backend calls AI vision adapter for candidate dish/ingredients/portion/confidence.
4. Ingredients normalized against local ingredient catalog.
5. Nutrition totals are calculated deterministically from nutrition tables.
6. Response includes uncertainty and editable items.
7. User confirms or edits and saves final meal.

## Bounded Services
- API service: business orchestration, auth, persistence.
- Worker service: async recommendation generation, report snapshots.
- ML services: model adapters for future replaceable inference.
