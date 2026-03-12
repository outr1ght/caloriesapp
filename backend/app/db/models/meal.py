from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import ModelBase
from app.db.models.domain_enums import AnalysisStatus, MealPlanStatus, MealSource, MealType, UploadStatus
from app.db.models.mixins import SoftDeleteMixin


class Meal(ModelBase, SoftDeleteMixin):
    __tablename__ = "meals"
    __table_args__ = (Index("ix_meals__user_id_eaten_at", "user_id", "eaten_at"), Index("ix_meals__analysis_status", "analysis_status"))

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    meal_type: Mapped[MealType] = mapped_column(Enum(MealType, name="meal_type", native_enum=False), nullable=False)
    source: Mapped[MealSource] = mapped_column(Enum(MealSource, name="meal_source", native_enum=False), nullable=False, default=MealSource.MANUAL, server_default=MealSource.MANUAL.value)
    eaten_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    analysis_status: Mapped[AnalysisStatus] = mapped_column(Enum(AnalysisStatus, name="analysis_status", native_enum=False), nullable=False, default=AnalysisStatus.READY, server_default=AnalysisStatus.READY.value)
    nutrition_value_id: Mapped[str | None] = mapped_column(ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    nutrition_value = relationship("NutritionValue", lazy="joined")
    items: Mapped[list["MealItem"]] = relationship(back_populates="meal", cascade="all, delete-orphan", passive_deletes=True)
    uploaded_images: Mapped[list["UploadedImage"]] = relationship(back_populates="meal", cascade="save-update")


class MealItem(ModelBase):
    __tablename__ = "meal_items"
    __table_args__ = (CheckConstraint("quantity > 0", name="meal_items_quantity_positive"), Index("ix_meal_items__meal_id_position", "meal_id", "position"))

    meal_id: Mapped[str] = mapped_column(ForeignKey("meals.id", ondelete="CASCADE"), nullable=False, index=True)
    ingredient_id: Mapped[str | None] = mapped_column(ForeignKey("ingredients.id", ondelete="SET NULL"), nullable=True)
    food_product_id: Mapped[str | None] = mapped_column(ForeignKey("food_products.id", ondelete="SET NULL"), nullable=True)
    nutrition_value_id: Mapped[str | None] = mapped_column(ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False, default="g", server_default="g")
    position: Mapped[int] = mapped_column(nullable=False, default=0, server_default="0")

    meal: Mapped["Meal"] = relationship(back_populates="items")


class UploadedImage(ModelBase, SoftDeleteMixin):
    __tablename__ = "uploaded_images"
    __table_args__ = (
        UniqueConstraint("storage_key", name="uq_uploaded_images__storage_key"),
        Index("ix_uploaded_images__user_id_created_at", "user_id", "created_at"),
        Index("ix_uploaded_images__sha256", "sha256"),
    )

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_id: Mapped[str | None] = mapped_column(ForeignKey("meals.id", ondelete="SET NULL"), nullable=True, index=True)
    storage_key: Mapped[str] = mapped_column(String(512), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[UploadStatus] = mapped_column(Enum(UploadStatus, name="upload_status", native_enum=False), nullable=False, default=UploadStatus.UPLOADED, server_default=UploadStatus.UPLOADED.value)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    meal: Mapped["Meal | None"] = relationship(back_populates="uploaded_images")


class MealPlan(ModelBase, SoftDeleteMixin):
    __tablename__ = "meal_plans"
    __table_args__ = (UniqueConstraint("user_id", "plan_date", name="uq_meal_plans__user_id_plan_date"), Index("ix_meal_plans__user_id_plan_date", "user_id", "plan_date"))

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[MealPlanStatus] = mapped_column(Enum(MealPlanStatus, name="meal_plan_status", native_enum=False), nullable=False, default=MealPlanStatus.DRAFT, server_default=MealPlanStatus.DRAFT.value)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    target_nutrition_value_id: Mapped[str | None] = mapped_column(ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True)
    meals_snapshot: Mapped[list[dict[str, Any]] | None] = mapped_column(JSONB, nullable=True)
