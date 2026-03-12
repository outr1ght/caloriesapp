"""initial schema

Revision ID: 20260312_0001
Revises: None
Create Date: 2026-03-12 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260312_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
        sa.Column("role", sa.Enum("user", "admin", name="user_role", native_enum=False), nullable=False, server_default="user"),
        sa.Column("locale", sa.Enum("en", "es", "ru", name="language_code", native_enum=False), nullable=False, server_default="en"),
        sa.Column("timezone", sa.String(length=64), nullable=False, server_default="UTC"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("email", name="uq_users__email"),
    )

    op.create_table(
        "auth_identities",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider", sa.Enum("local", "google", "apple", name="auth_provider", native_enum=False), nullable=False),
        sa.Column("provider_user_id", sa.String(length=255), nullable=False),
        sa.Column("provider_email", sa.String(length=320), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("provider", "provider_user_id", name="uq_auth_identities__provider_provider_user_id"),
    )

    op.create_table(
        "user_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=True),
        sa.Column("birth_year", sa.Integer(), nullable=True),
        sa.Column("gender", sa.String(length=32), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", name="uq_user_profiles__user_id"),
    )

    op.create_table(
        "nutrition_values",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("calories", sa.Numeric(10, 2), nullable=False),
        sa.Column("protein_g", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("carbs_g", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("fat_g", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("fiber_g", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("sugar_g", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("sodium_mg", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("serving_size_g", sa.Numeric(10, 2), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=False, server_default="deterministic"),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "ingredients",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("default_nutrition_value_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("name", name="uq_ingredients__name"),
    )

    op.create_table(
        "food_products",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("brand", sa.String(length=255), nullable=True),
        sa.Column("source_name", sa.String(length=64), nullable=False, server_default="internal"),
        sa.Column("source_product_id", sa.String(length=255), nullable=True),
        sa.Column("default_nutrition_value_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("source_name", "source_product_id", name="uq_food_products__source_name_source_product_id"),
    )

    op.create_table(
        "barcodes",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("food_product_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("food_products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("format", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("code", name="uq_barcodes__code"),
    )

    op.create_table(
        "meals",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.String(length=2048), nullable=True),
        sa.Column("meal_type", sa.Enum("breakfast", "lunch", "dinner", "snack", "other", name="meal_type", native_enum=False), nullable=False),
        sa.Column("source", sa.Enum("manual", "barcode", "image_analysis", "imported", name="meal_source", native_enum=False), nullable=False, server_default="manual"),
        sa.Column("eaten_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("analysis_status", sa.Enum("pending", "processing", "ready", "failed", name="analysis_status", native_enum=False), nullable=False, server_default="ready"),
        sa.Column("nutrition_value_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "meal_items",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("meal_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("meals.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ingredient_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("ingredients.id", ondelete="SET NULL"), nullable=True),
        sa.Column("food_product_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("food_products.id", ondelete="SET NULL"), nullable=True),
        sa.Column("nutrition_value_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 3), nullable=False),
        sa.Column("unit", sa.String(length=32), nullable=False, server_default="g"),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "uploaded_images",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("meal_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("meals.id", ondelete="SET NULL"), nullable=True),
        sa.Column("storage_key", sa.String(length=512), nullable=False),
        sa.Column("mime_type", sa.String(length=128), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("status", sa.Enum("uploaded", "scanned", "rejected", name="upload_status", native_enum=False), nullable=False, server_default="uploaded"),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("storage_key", name="uq_uploaded_images__storage_key"),
    )

    op.create_table(
        "nutrition_goals",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("strategy", sa.Enum("maintain", "lose", "gain", name="goal_strategy", native_enum=False), nullable=False),
        sa.Column("activity_level", sa.Enum("sedentary", "light", "moderate", "active", "very_active", name="activity_level", native_enum=False), nullable=False),
        sa.Column("target_calories", sa.Numeric(10, 2), nullable=False),
        sa.Column("target_protein_g", sa.Numeric(10, 2), nullable=True),
        sa.Column("target_carbs_g", sa.Numeric(10, 2), nullable=True),
        sa.Column("target_fat_g", sa.Numeric(10, 2), nullable=True),
        sa.Column("target_water_ml", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("meal_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("meals.id", ondelete="SET NULL"), nullable=True),
        sa.Column("recommendation_type", sa.Enum("meal_adjustment", "daily_summary", "goal_alignment", "hydration", name="recommendation_type", native_enum=False), nullable=False),
        sa.Column("status", sa.Enum("pending", "ready", "dismissed", "applied", name="recommendation_status", native_enum=False), nullable=False, server_default="pending"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.String(length=4096), nullable=False),
        sa.Column("generator", sa.String(length=64), nullable=False, server_default="hybrid"),
        sa.Column("rationale_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("context_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "weight_logs",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("logged_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("weight_kg", sa.Numeric(6, 2), nullable=False),
        sa.Column("body_fat_percent", sa.Numeric(5, 2), nullable=True),
        sa.Column("note", sa.String(length=512), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", "logged_at", name="uq_weight_logs__user_id_logged_at"),
    )

    op.create_table(
        "meal_plans",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.Enum("draft", "active", "archived", name="meal_plan_status", native_enum=False), nullable=False, server_default="draft"),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.String(length=2048), nullable=True),
        sa.Column("target_nutrition_value_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True),
        sa.Column("meals_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", "plan_date", name="uq_meal_plans__user_id_plan_date"),
    )

    op.create_table(
        "user_settings",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("language", sa.Enum("en", "es", "ru", name="language_code_settings", native_enum=False), nullable=False, server_default="en"),
        sa.Column("unit_system", sa.Enum("metric", "imperial", name="unit_system", native_enum=False), nullable=False, server_default="metric"),
        sa.Column("notifications_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("meal_reminder_enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("privacy_flags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("feature_flags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", name="uq_user_settings__user_id"),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.Enum("create", "update", "delete", "login", "logout", "export", name="audit_action", native_enum=False), nullable=False),
        sa.Column("entity_type", sa.String(length=128), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("request_id", sa.String(length=64), nullable=True),
        sa.Column("ip_hash", sa.String(length=128), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("user_settings")
    op.drop_table("meal_plans")
    op.drop_table("weight_logs")
    op.drop_table("recommendations")
    op.drop_table("nutrition_goals")
    op.drop_table("uploaded_images")
    op.drop_table("meal_items")
    op.drop_table("meals")
    op.drop_table("barcodes")
    op.drop_table("food_products")
    op.drop_table("ingredients")
    op.drop_table("nutrition_values")
    op.drop_table("user_profiles")
    op.drop_table("auth_identities")
    op.drop_table("users")
