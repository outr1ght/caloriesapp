# Nutrition Assistant Backend

Production-oriented FastAPI backend.

## Stack
- FastAPI
- SQLAlchemy 2.x async
- Alembic
- PostgreSQL
- Redis
- Celery
- JWT auth + refresh token rotation
- OpenAI integration wrapper
- S3-compatible upload abstraction

## Setup
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e .
copy .env.example .env
```

## Run API
```bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Health endpoint:
- `GET /api/v1/health`

## Run worker
```bash
celery -A app.worker.celery_app.celery_app worker -l INFO
```

## Tests
```bash
pytest -q
```

## Key env vars
- `APP_SECRET_KEY`
- `APP_DATABASE_URL`
- `APP_REDIS_URL`
- `APP_OPENAI_API_KEY`
- `APP_OPENAI_MODEL`
- `APP_S3_ENDPOINT_URL`
- `APP_S3_BUCKET`
- `APP_S3_ACCESS_KEY_ID`
- `APP_S3_SECRET_ACCESS_KEY`

## Notes
- AI outputs are schema-validated where wrappers are used.
- Meal nutrition totals are deterministic; AI is used for reasoning/explanation.
