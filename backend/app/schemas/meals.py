from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.domain_enums import AnalysisStatus, MealSource, MealType


class NutritionValueDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str | None = None
    calories: Decimal = Field(ge=0)
    protein_g: Decimal = Field(ge=0)
    carbs_g: Decimal = Field(ge=0)
    fat_g: Decimal = Field(ge=0)
    fiber_g: Decimal = Field(ge=0, default=Decimal("0"))
    sugar_g: Decimal = Field(ge=0, default=Decimal("0"))
    sodium_mg: Decimal = Field(ge=0, default=Decimal("0"))
    serving_size_g: Decimal | None = Field(default=None, ge=0)
    source: str = "deterministic"
    confidence: Decimal | None = Field(default=None, ge=0, le=1)


class MealItemCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ingredient_id: str | None = None
    food_product_id: str | None = None
    display_name: str = Field(min_length=1, max_length=255)
    quantity: Decimal = Field(gt=0)
    unit: str = Field(default="g", min_length=1, max_length=32)
    position: int = Field(default=0, ge=0)
    nutrition: NutritionValueDTO | None = None


class MealCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=2048)
    meal_type: MealType
    source: MealSource = MealSource.MANUAL
    eaten_at: datetime
    items: list[MealItemCreateRequest] = Field(default_factory=list, min_length=1)


class MealUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=2048)
    meal_type: MealType | None = None
    eaten_at: datetime | None = None


class MealListQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")
    from_dt: datetime | None = None
    to_dt: datetime | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class MealDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    user_id: str
    title: str | None
    notes: str | None
    meal_type: MealType
    source: MealSource
    eaten_at: datetime
    analysis_status: AnalysisStatus
    created_at: datetime
    updated_at: datetime
