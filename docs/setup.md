# Setup

## Prerequisites

- Windows with PowerShell
- Python 3.11+ installed and available in `PATH`
- Docker Desktop with `docker compose` for reproducible local PostgreSQL/Redis/MinIO
- Node.js 20+ with `npm` available in `PATH` for commit tooling

## Recommended bootstrap

From the repository root run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1 -StartInfrastructure
```

What the script does:

- creates `backend/.env` from `backend/.env.example` if missing
- starts local `postgres`, `redis`, and `minio` with Docker Compose when `-StartInfrastructure` is passed
- recreates `backend/venv`
- upgrades `pip`
- installs `backend/requirements.txt`
- verifies `pytest`
- verifies `alembic heads`
- attempts `alembic upgrade head`

If Docker is not installed, run the script without `-StartInfrastructure` and provide PostgreSQL/Redis manually.

## One-command backend quality gate

From the repository root:

```powershell
.\scripts\check-backend.ps1
```

What the script validates:

- starts local `postgres`, `redis`, and `minio`
- runs `alembic upgrade head`
- runs `alembic current`
- runs `python -m pytest`
- performs `/api/v1/health` check if backend is already running on `127.0.0.1:8000`

## Conventional Commits validation

From the repository root:

```powershell
npm install
```

This installs local commit tooling and enables the `commit-msg` hook via Husky.

Manual validation examples:

```powershell
echo "bad message" | npx commitlint
echo "feat: add backend quality gate" | npx commitlint
```

Expected behavior:

- invalid messages are rejected
- valid Conventional Commits pass
- local `git commit` is checked by `.husky/commit-msg`

Supported commit types:

- `feat:`
- `fix:`
- `docs:`
- `test:`
- `refactor:`
- `chore:`
- `ci:`
- `build:`

Examples:

- `feat: add backend quality gate`
- `fix: handle upload checksum mismatch`
- `docs: document local backend setup`
- `ci: add backend workflow`

## Docker-first local database verification

From the repository root:

```powershell
docker compose -f .\infrastructure\docker-compose.yml up -d postgres redis minio
cd .\backend
.\venv\Scripts\activate
alembic upgrade head
alembic current
python -m pytest
```

Expected outcome:

- PostgreSQL listens on `localhost:5432`
- Redis listens on `localhost:6379`
- Alembic upgrades to the current head without connection errors
- `python -m pytest` completes against the local backend environment

## Manual Python setup

From the repository root:

```powershell
python --version
Copy-Item .\backend\.env.example .\backend\.env
python -m venv backend/venv
.\backend\venv\Scripts\activate
pip install -r .\backend\requirements.txt
```

## Run tests

```powershell
cd .\backend
.\venv\Scripts\activate
python -m pytest
```

## Alembic

```powershell
cd .\backend
.\venv\Scripts\activate
alembic heads
alembic upgrade head
alembic current
```

Notes:

- `alembic heads` works without database access
- `alembic upgrade head` and `alembic current` require reachable PostgreSQL from `APP_DATABASE_URL`
- default local settings come from `backend/.env` and point to `localhost`

## Run backend

```powershell
cd .\backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Verify backend

In another terminal:

```powershell
curl http://127.0.0.1:8000/api/v1/health
curl http://127.0.0.1:8000/docs
```

Expected responses:

- `/api/v1/health` returns HTTP 200 with the standard JSON envelope
- `/docs` returns HTTP 200 and serves Swagger UI

## OpenAPI export

From the repository root:

```powershell
.\scripts\export-openapi.ps1
```

What the script does:

- imports the FastAPI app without starting the server
- writes the generated schema to `docs/openapi/openapi.json` using the current `backend/.env` configuration
- validates required mobile-integration paths and schemas

Flutter consumption guidance:

- use `docs/openapi/openapi.json` as the canonical backend contract snapshot
- regenerate it after backend contract changes before mobile client code generation
- use it for DTO/client generation and contract review, but keep runtime tests as the final source of truth

