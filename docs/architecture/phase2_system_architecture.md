# Phase 2: System Architecture and Data Flow

## Architecture Goals
- Fast, low-friction logging from camera.
- Deterministic nutrition totals for consistency.
- Explicit uncertainty and user correction.
- Global-first localization across app and backend.
- Service boundaries that are easy to scale independently.

## Runtime Components
- Flutter mobile app (`/mobile_app`)
  - Presentation/Application/Domain/Data layers by feature.
  - Riverpod state and go_router navigation.
- FastAPI API (`/backend`)
  - API transport (`app/api/v1/endpoints`)
  - service orchestration (`app/services`)
  - repositories (`app/db/repositories`)
  - persistence models + migrations (`app/db/models`, `alembic`)
- AI/CV microservices (`/ml_services`)
  - meal vision service
  - ingredient classification service
  - portion estimation service
- Infrastructure (`/infrastructure`)
  - Docker Compose local stack
  - Kubernetes deployment baseline

## Data Flow: Photo Meal Analysis
1. User captures photo on device.
2. Flutter uploads image to `/api/v1/uploads/image`.
3. Backend validates MIME/size and writes metadata row in `uploaded_images`.
4. Backend invokes analysis pipeline:
   - CV/vision inference for dish + ingredients + confidence
   - ingredient normalization against internal catalog
   - deterministic nutrition mapping from `nutrition_values`
5. API responds with:
   - `analysis_confidence`
   - `requires_manual_review`
   - editable ingredient items and nutrition totals
6. User edits/corrects items in mobile screen.
7. Flutter sends corrected payload to `/api/v1/meals`.
8. Backend persists `meals` and `meal_items` as final source of truth.

## Data Flow: Barcode Scan
1. User scans barcode in mobile.
2. Flutter posts barcode code to `/api/v1/barcodes/scan`.
3. Backend searches local `barcodes` + `food_products`.
4. Optional external lookup adapter if local miss.
5. Normalized product response returned for user confirmation.
6. User saves as meal entry mapped into `meals` + `meal_items`.

## Data Flow: Reports
1. Flutter requests daily/weekly/monthly endpoints.
2. Backend aggregates `meal_items` grouped by date range and timezone.
3. Response includes calories/macros + goal deviation.
4. Mobile renders readable charts with localized labels.

## Hybrid AI Pipeline Boundaries
- Layer 1: perception (vision) -> probabilistic outputs.
- Layer 2: reasoning (ingredient candidates) -> constrained JSON outputs.
- Layer 3: deterministic nutrition mapping -> final numeric totals.
- Layer 4: recommendation text generation -> localized and concise.

## Uncertainty Handling Contract
- Ingredient-level `confidence` (0..1)
- Meal-level `analysis_confidence` (0..1)
- `requires_manual_review=true` when confidence threshold breached.
- Save flow should block direct save unless user confirms edits.

## API and Model Consistency Rules
- API DTOs use the same enum vocabulary as DB domain:
  - meal type, locale, unit system, auth provider
- Mobile data layer maps DTO fields 1:1 for core entities.
- Backward compatible API changes are additive only in v1.

## Repository Layout (Phase 2)
- `/mobile_app`: feature-first clean architecture.
- `/backend`: modular API/service/repository structure.
- `/ml_services`: swappable inference adapters.
- `/infrastructure`: local + deployment scaffolding.
- `/docs`: executable product/architecture specs.
