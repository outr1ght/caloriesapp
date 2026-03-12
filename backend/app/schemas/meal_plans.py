from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.domain_enums import MealPlanStatus, MealType


class MealPlanEntryDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    meal_type: MealType
    title: str = Field(min_length=1, max_length=255)


class MealPlanCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    plan_date: datetime
    title: str | None = None
    notes: str | None = None
    status: MealPlanStatus = MealPlanStatus.DRAFT
    entries: list[MealPlanEntryDTO] = Field(default_factory=list)


class MealPlanUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = None
    notes: str | None = None
    status: MealPlanStatus | None = None
    entries: list[MealPlanEntryDTO] | None = None
