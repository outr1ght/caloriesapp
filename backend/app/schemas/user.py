from datetime import datetime
from pydantic import BaseModel, Field


class ProfilePatch(BaseModel):
    age: int | None = Field(default=None, ge=1, le=120)
    sex: str | None = None
    height_cm: int | None = Field(default=None, ge=50, le=260)
    weight_kg: float | None = Field(default=None, ge=20, le=400)
    activity_level: str | None = None
    dietary_preference: str | None = None


class GoalsPatch(BaseModel):
    calorie_target: int = Field(ge=800, le=6000)
    protein_target_g: int | None = Field(default=None, ge=0, le=500)
    fat_target_g: int | None = Field(default=None, ge=0, le=500)
    carbs_target_g: int | None = Field(default=None, ge=0, le=1000)


class SettingsPatch(BaseModel):
    locale: str = Field(pattern="^(en|es|de|fr|ru)$")
    unit_system: str = Field(pattern="^(metric|imperial)$")


class MeResponse(BaseModel):
    user_id: str
    email: str
    locale: str
    unit_system: str


class WeightCreate(BaseModel):
    measured_at: datetime
    weight_kg: float = Field(ge=20, le=400)
