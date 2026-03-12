from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.common import TimestampMixin, UUIDMixin
from app.db.models.enums import AuthProvider, LocaleCode, MealType, RecommendationType


class UploadedImage(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "uploaded_images"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    s3_key: Mapped[str] = mapped_column(String(512), unique=True)
    mime_type: Mapped[str] = mapped_column(String(64))
    size_bytes: Mapped[int]


class Ingredient(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ingredients"

    canonical_name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255))


class NutritionValue(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "nutrition_values"

    ingredient_id: Mapped[str] = mapped_column(String(36), ForeignKey("ingredients.id"), unique=True)
    calories_per_100g: Mapped[float] = mapped_column(Float)
    protein_per_100g: Mapped[float] = mapped_column(Float)
    fat_per_100g: Mapped[float] = mapped_column(Float)
    carbs_per_100g: Mapped[float] = mapped_column(Float)


class Meal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "meals"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    meal_type: Mapped[MealType] = mapped_column(Enum(MealType, native_enum=False), index=True)
    consumed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), index=True)
    image_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("uploaded_images.id"), nullable=True)
    analysis_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class MealItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "meal_items"

    meal_id: Mapped[str] = mapped_column(String(36), ForeignKey("meals.id"), index=True)
    ingredient_id: Mapped[str] = mapped_column(String(36), ForeignKey("ingredients.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    grams: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    calories: Mapped[float] = mapped_column(Float)
    protein_g: Mapped[float] = mapped_column(Float)
    fat_g: Mapped[float] = mapped_column(Float)
    carbs_g: Mapped[float] = mapped_column(Float)
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Recommendation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "recommendations"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    locale: Mapped[LocaleCode] = mapped_column(Enum(LocaleCode, native_enum=False), default=LocaleCode.EN)
    recommendation_type: Mapped[RecommendationType] = mapped_column(Enum(RecommendationType, native_enum=False))
    confidence: Mapped[float] = mapped_column(Float)
    summary: Mapped[str] = mapped_column(Text)


class WeightLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "weight_logs"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    measured_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), index=True)
    weight_kg: Mapped[float] = mapped_column(Float)
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class FoodProduct(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "food_products"

    name: Mapped[str] = mapped_column(String(255))
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    serving_size_g: Mapped[float | None] = mapped_column(Float, nullable=True)
    calories_per_100g: Mapped[float] = mapped_column(Float)
    protein_per_100g: Mapped[float] = mapped_column(Float)
    fat_per_100g: Mapped[float] = mapped_column(Float)
    carbs_per_100g: Mapped[float] = mapped_column(Float)


class Barcode(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "barcodes"

    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("food_products.id"), index=True)


class MealPlan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "meal_plans"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    locale: Mapped[LocaleCode] = mapped_column(Enum(LocaleCode, native_enum=False), default=LocaleCode.EN)
    plan_json: Mapped[str] = mapped_column(Text)
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AuthIdentity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "auth_identities"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    provider: Mapped[AuthProvider] = mapped_column(Enum(AuthProvider, native_enum=False), index=True)
    provider_subject: Mapped[str] = mapped_column(String(255), index=True)


class Translation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "translations"

    locale: Mapped[LocaleCode] = mapped_column(Enum(LocaleCode, native_enum=False), index=True)
    key: Mapped[str] = mapped_column(String(255), index=True)
    value: Mapped[str] = mapped_column(Text)


class AuditLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(128), index=True)
    resource_type: Mapped[str] = mapped_column(String(64), index=True)
    resource_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
