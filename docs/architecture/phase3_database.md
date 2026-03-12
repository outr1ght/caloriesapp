# Phase 3: Database Design and Migration Strategy

## Naming Conventions
- Tables: snake_case plural (`meal_items`).
- Primary keys: `id` (UUID string in MVP scaffold).
- Foreign keys: `<entity>_id`.
- Timestamps: `created_at`, `updated_at`.
- Soft delete: `deleted_at` where user-managed historical data exists.

## Enum Strategy
Enums are stored as strings for portability:
- `locale`: en/es/de/fr/ru
- `unit_system`: metric/imperial
- `meal_type`: breakfast/lunch/dinner/snack
- `auth_provider`: password/google/apple

## Required Tables Implemented
- users
- auth_identities
- user_profiles
- nutrition_goals
- user_settings
- uploaded_images
- ingredients
- nutrition_values
- meals
- meal_items
- recommendations
- weight_logs
- food_products
- barcodes
- meal_plans
- translations
- audit_logs

## ERD (Text)
- users 1--N auth_identities
- users 1--1 user_profiles
- users 1--1 nutrition_goals
- users 1--1 user_settings
- users 1--N uploaded_images
- users 1--N meals
- meals 1--N meal_items
- ingredients 1--1 nutrition_values
- meal_items N--1 ingredients
- users 1--N recommendations
- users 1--N weight_logs
- food_products 1--N barcodes
- users 1--N meal_plans
- users 1--N audit_logs

## Indexing Strategy
- Identity lookups: users.email, auth_identities(provider, provider_subject)
- Timeline queries: meals(consumed_at), weight_logs(measured_at)
- FK joins: all `*_id` columns indexed on high-traffic tables
- Search keys: ingredients.canonical_name, barcodes.code

## Uniqueness Strategy
- users.email
- auth_identities(provider, provider_subject)
- one profile/goal/settings per user (`user_id` unique)
- ingredients.canonical_name
- nutrition_values.ingredient_id
- uploaded_images.s3_key
- barcodes.code
- translations(locale, key)

## Migration Plan
1. `0001_initial` creates full baseline schema.
2. Next migration adds optional partitioning for meal/audit tables.
3. Future migration introduces numeric PKs or UUID native type if needed.
4. Data migrations for enum expansions remain backward compatible.

## Seed Data Strategy
- Seed minimal canonical ingredients + nutrition values.
- Seed one demo barcode/product pair for local testing.
- Keep seed idempotent by checking unique keys before insert.

## Query Patterns
- Daily totals: sum meal_items by consumed_at date boundary.
- Weekly/monthly trends: grouped aggregates with timezone-aware windows.
- Recommendations trigger input: rolling 7-day aggregates.
