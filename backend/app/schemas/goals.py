from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.domain_enums import ActivityLevel, GoalStrategy


class NutritionGoalCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    strategy: GoalStrategy
    activity_level: ActivityLevel
    target_calories: Decimal = Field(gt=0)
    target_protein_g: Decimal | None = Field(default=None, ge=0)
    target_carbs_g: Decimal | None = Field(default=None, ge=0)
    target_fat_g: Decimal | None = Field(default=None, ge=0)
    target_water_ml: int | None = Field(default=None, ge=0)
    effective_from: datetime


class NutritionGoalUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    strategy: GoalStrategy | None = None
    activity_level: ActivityLevel | None = None
    target_calories: Decimal | None = Field(default=None, gt=0)
    target_protein_g: Decimal | None = Field(default=None, ge=0)
    target_carbs_g: Decimal | None = Field(default=None, ge=0)
    target_fat_g: Decimal | None = Field(default=None, ge=0)
    target_water_ml: int | None = Field(default=None, ge=0)
    effective_to: datetime | None = None
    is_active: bool | None = None


class NutritionGoalDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    id: str
    user_id: str
    strategy: GoalStrategy
    activity_level: ActivityLevel
    target_calories: Decimal
    target_protein_g: Decimal | None
    target_carbs_g: Decimal | None
    target_fat_g: Decimal | None
    target_water_ml: int | None
    is_active: bool
    effective_from: datetime
    effective_to: datetime | None
    created_at: datetime
    updated_at: datetime
