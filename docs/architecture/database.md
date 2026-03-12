# Database Design

## ERD (Text)
- users (1) -> (N) auth_identities
- users (1) -> (1) user_profiles
- users (1) -> (1) nutrition_goals
- users (1) -> (1) user_settings
- users (1) -> (N) meals
- meals (1) -> (N) meal_items
- meal_items (N) -> (1) ingredients
- ingredients (1) -> (1) nutrition_values
- meals (1) -> (1) uploaded_images
- users (1) -> (N) recommendations
- users (1) -> (N) weight_logs
- food_products (1) -> (N) barcodes
- users (1) -> (N) meal_plans
- users (1) -> (N) audit_logs

## Migration Strategy
- Alembic for forward-only migrations.
- Separate schema and seed scripts.
- Naming convention for constraints and indexes.

## Soft Delete
- `deleted_at` on user-editable entities (`meals`, `meal_items`, `weight_logs`, `meal_plans`).
