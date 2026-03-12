# Nutrition Assistant Backend

Production-oriented FastAPI backend for the nutrition assistant application.

## Stack

- FastAPI
- SQLAlchemy 2.x (async)
- Alembic
- PostgreSQL
- Redis
- Celery
- JWT auth
- OAuth-ready provider model (Google/Apple)
- S3-compatible storage abstraction
- OpenAI integration abstraction

## Local Run

1. `pip install -e .`
2. `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
3. Worker: `celery -A app.worker.celery_app.celery_app worker -l INFO`

## Test Run

- `pytest -q`
