from datetime import date
from pydantic import BaseModel, Field


class NutritionSnapshot(BaseModel):
    calories: float = Field(ge=0)
    protein_g: float = Field(ge=0)
    fat_g: float = Field(ge=0)
    carbs_g: float = Field(ge=0)


class MealItemContract(BaseModel):
    ingredient_id: str
    name: str = Field(min_length=1, max_length=255)
    grams: float = Field(gt=0, le=2500)
    confidence: float | None = Field(default=None, ge=0, le=1)
    nutrition: NutritionSnapshot


class MealContract(BaseModel):
    id: str
    user_id: str
    meal_type: str
    consumed_at: date
    analysis_confidence: float | None = Field(default=None, ge=0, le=1)
    items: list[MealItemContract] = Field(default_factory=list)


class ReportContract(BaseModel):
    period: str
    start_date: date
    end_date: date
    nutrition: NutritionSnapshot
