from decimal import Decimal
from typing import Any

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import ModelBase
from app.db.models.mixins import SoftDeleteMixin


class NutritionValue(ModelBase):
    __tablename__ = "nutrition_values"
    __table_args__ = (
        CheckConstraint("calories >= 0", name="nutrition_values_calories_non_negative"),
        CheckConstraint("protein_g >= 0", name="nutrition_values_protein_non_negative"),
        CheckConstraint("carbs_g >= 0", name="nutrition_values_carbs_non_negative"),
        CheckConstraint("fat_g >= 0", name="nutrition_values_fat_non_negative"),
    )

    calories: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    protein_g: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    carbs_g: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    fat_g: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    fiber_g: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    sugar_g: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    sodium_mg: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    serving_size_g: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="deterministic")
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(4, 3), nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)


class Ingredient(ModelBase, SoftDeleteMixin):
    __tablename__ = "ingredients"
    __table_args__ = (UniqueConstraint("name", name="uq_ingredients__name"), Index("ix_ingredients__name", "name"))

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    default_nutrition_value_id: Mapped[str | None] = mapped_column(ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True)

    default_nutrition: Mapped["NutritionValue | None"] = relationship(lazy="joined")


class FoodProduct(ModelBase, SoftDeleteMixin):
    __tablename__ = "food_products"
    __table_args__ = (
        UniqueConstraint("source_name", "source_product_id", name="uq_food_products__source_name_source_product_id"),
        Index("ix_food_products__name_brand", "name", "brand"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_name: Mapped[str] = mapped_column(String(64), nullable=False, default="internal")
    source_product_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    default_nutrition_value_id: Mapped[str | None] = mapped_column(ForeignKey("nutrition_values.id", ondelete="SET NULL"), nullable=True)

    default_nutrition: Mapped["NutritionValue | None"] = relationship(lazy="joined")
    barcodes: Mapped[list["Barcode"]] = relationship("Barcode", back_populates="food_product", cascade="all, delete-orphan", passive_deletes=True)


class Barcode(ModelBase):
    __tablename__ = "barcodes"
    __table_args__ = (UniqueConstraint("code", name="uq_barcodes__code"), Index("ix_barcodes__code", "code"))

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    food_product_id: Mapped[str] = mapped_column(ForeignKey("food_products.id", ondelete="CASCADE"), nullable=False, index=True)
    format: Mapped[str | None] = mapped_column(String(32), nullable=True)

    food_product: Mapped["FoodProduct"] = relationship(back_populates="barcodes")
