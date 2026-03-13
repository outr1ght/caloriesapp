# CaloriesApp Monorepo

AI-first nutrition assistant monorepo with FastAPI backend and Flutter mobile app.

## Repository
- `backend`: FastAPI API, Alembic migrations, Celery worker
- `mobile_app`: Flutter app (Riverpod + go_router + Dio)
- `infrastructure`: local docker-compose stack for postgres/redis/minio/backend/worker
- `docs`: architecture, API, release and product docs

## Local prerequisites
- Docker + Docker Compose
- Python 3.11+
- Flutter 3.24+

## Quickstart (local)

### 1) Start infra and backend containers
```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Backend API:
- `http://localhost:8000/api/v1/health`

### 2) Backend local (without docker backend)
```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate
pip install -e .
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Worker:
```bash
celery -A app.worker.celery_app.celery_app worker -l INFO
```

### 3) Flutter app
```bash
cd mobile_app
flutter pub get
flutter gen-l10n
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1
```

## Test commands
- Backend: `cd backend && pytest -q`
- Mobile: `cd mobile_app && flutter test`

## Environment and ports
- Backend API: `8000`
- PostgreSQL: `5432`
- Redis: `6379`
- MinIO API/console: `9000` / `9001`

## Known MVP limitations
- Nutrition estimates are approximate and user-editable.
- AI explanation text can degrade under provider outages (fallback warnings are returned).
- Production monitoring (Sentry/alerts) is scaffolded but requires project credentials.

## Pre-release checklist
- Apply migrations on target environment.
- Verify S3 bucket and credentials.
- Verify OpenAI API key and model in backend env.
- Run backend and mobile tests.
- Validate auth refresh flow and protected endpoints from mobile.

Launch notes: docs/release/launch_readiness.md

