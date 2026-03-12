# CaloriesApp Monorepo

AI-first global nutrition assistant MVP monorepo.

## 1) Product brief
CaloriesApp is a cross-platform nutrition assistant that lets users capture meals from photos, review AI-detected ingredients, correct portions, and track calories/macros over time. The product is intentionally **non-medical** and all nutrition estimates are approximate and user-editable.

## 2) Target users and use cases
- Busy professionals: fast meal logging from camera.
- Fitness-focused users: macro and calorie target tracking.
- Global users: multilingual UI and locale-aware units.
- Beginners: guided onboarding, recommendations, and meal plans.

Primary use cases:
- Log meal from image in under 30 seconds.
- Scan packaged food barcode and save to diary.
- View daily/weekly/monthly calorie and macro trends.
- Receive actionable recommendations in selected language.

## 3) MVP scope and non-goals
### MVP scope
- Auth (email/password + Google/Apple OAuth contract)
- Profile, goals, settings
- Photo upload + AI meal analysis + manual correction
- Food diary CRUD
- Daily/weekly/monthly reporting
- Recommendations and AI meal plan generation
- Barcode lookup abstraction + manual fallback
- Localization: EN, ES, DE, FR, RU

### Non-goals
- Medical diagnosis or treatment advice
- Clinical-grade nutrient precision
- Full offline-first nutrition intelligence
- Advanced social/community features

## 4) High-level architecture
- `mobile_app`: Flutter + Riverpod + go_router + Dio + l10n
- `backend`: FastAPI + SQLAlchemy 2.x + Alembic + Redis + Celery
- `ml_services`: Python inference microservices abstraction
- `infrastructure`: Docker, Compose, K8s-ready manifests, GitHub Actions
- Storage: PostgreSQL, Redis, S3-compatible object storage
- Observability: Sentry hooks, structured logs

## 5) Repository structure
```text
/mobile_app          Flutter app (clean architecture)
/backend             FastAPI API + domain services + workers
/ml_services         CV/ML abstraction and future model services
/infrastructure      docker-compose, Dockerfiles, k8s scaffolds
/docs                product, architecture, API, release docs
/tests               cross-system contract tests
/scripts             local automation (seed, lint, dev helpers)
```

## 6) Database schema overview
Core entities:
- users, auth_identities, user_profiles, nutrition_goals, user_settings
- meals, meal_items, ingredients, nutrition_values, uploaded_images
- recommendations, meal_plans, weight_logs
- food_products, barcodes
- translations (optional runtime localization overrides)
- audit_logs

See: [docs/architecture/database.md](docs/architecture/database.md)

## 7) Backend module map
- `auth`, `users/profiles/settings/goals`
- `uploads`, `meal_analysis`, `meals`
- `nutrition`, `reports`, `recommendations`
- `barcode`, `meal_plans`, `weights`, `localization`
- `core` (config, security, middleware), `db`, `workers`

See: [docs/architecture/backend.md](docs/architecture/backend.md)

## 8) Mobile architecture map
Clean architecture by feature:
- Presentation: widgets/screens + Riverpod providers
- Application: use cases
- Domain: entities/repository contracts
- Data: DTOs, API clients, repository impls

See: [docs/architecture/mobile.md](docs/architecture/mobile.md)

## 9) AI pipeline design (hybrid)
1. Vision analysis (dish/ingredients/portion candidates + confidence)
2. Ingredient normalization
3. Deterministic nutrition mapping (DB datasets)
4. Recommendation generation via OpenAI

Low-confidence outputs force explicit user review before save.

See: [docs/architecture/ai_pipeline.md](docs/architecture/ai_pipeline.md)

## 10) Internationalization strategy
- Flutter ARB files for EN/ES/DE/FR/RU
- Backend localized error messages via key-based catalog
- Locale auto-detection and manual switch
- Metric/imperial setting per user

See: [docs/architecture/i18n.md](docs/architecture/i18n.md)

## 11) Development roadmap by phases/sprints
### Sprint 1
- Auth, profile/goals/settings, base mobile shell, DB migrations
### Sprint 2
- Image upload, AI meal analysis, edit-and-save flow
### Sprint 3
- Diary, reports, recommendations, barcode flow
### Sprint 4
- Meal planner, localization hardening, QA, release prep

## Quickstart
### Requirements
- Docker + Docker Compose
- Flutter SDK 3.24+
- Python 3.12 available in PATH

### 1) Start platform dependencies
```bash
docker compose -f infrastructure/docker-compose.yml up -d postgres redis minio
```

### 2) Start backend API
```bash
cd backend
cp .env.example .env
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 3) Start Celery worker (new terminal)
```bash
cd backend
. .venv/Scripts/activate
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

### 4) Start meal vision microservice (new terminal)
```bash
cd ml_services/meal_vision_service
docker build -t calories-meal-vision .
docker run --rm -p 8100:8100 calories-meal-vision
```

### 5) Start Flutter app
```bash
cd mobile_app
flutter pub get
flutter gen-l10n
flutter run
```

### One-command local stack
```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

## Disclaimers
- Nutrition values are approximate.
- Meal recognition can be incorrect.
- This app is not a medical device.
- Users must verify critical dietary decisions.
