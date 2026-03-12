from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.common import PaginationMeta


class UploadImageResponse(BaseModel):
    image_id: str
    upload_url: str


class MealAnalysisRequest(BaseModel):
    image_id: str
    meal_type: str = Field(pattern="^(breakfast|lunch|dinner|snack)$")
    consumed_at: datetime


class MealItemIn(BaseModel):
    name: str
    grams: float = Field(gt=0, le=2500)
    confidence: float | None = Field(default=None, ge=0, le=1)


class NutritionTotals(BaseModel):
    calories: float
    protein_g: float
    fat_g: float
    carbs_g: float


class MealAnalysisResponse(BaseModel):
    analysis_id: str
    analysis_confidence: float = Field(ge=0, le=1)
    requires_manual_review: bool
    items: list[MealItemIn]
    nutrition: NutritionTotals
    disclaimer_key: str = "nutrition.approximate"


class MealCreateRequest(BaseModel):
    meal_type: str = Field(pattern="^(breakfast|lunch|dinner|snack)$")
    consumed_at: datetime
    image_id: str | None = None
    items: list[MealItemIn]


class MealPatchRequest(MealCreateRequest):
    pass


class MealResponse(BaseModel):
    meal_id: str
    meal_type: str
    consumed_at: datetime
    items: list[MealItemIn]
    nutrition: NutritionTotals


class MealListResponse(BaseModel):
    items: list[MealResponse]
    pagination: PaginationMeta
