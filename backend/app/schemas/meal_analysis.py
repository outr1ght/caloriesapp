from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.domain_enums import AnalysisStatus


class MealAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    meal_id: str | None = None
    uploaded_image_ids: list[str] = Field(default_factory=list, min_length=1)


class MealAnalysisCandidateItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    estimated_quantity: Decimal
    unit: str
    confidence: Decimal


class MealAnalysisNutrition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    calories: Decimal
    protein_g: Decimal
    carbs_g: Decimal
    fat_g: Decimal
    confidence: Decimal


class MealAnalysisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    meal_id: str
    status: AnalysisStatus
    analyzed_at: datetime
    items: list[MealAnalysisCandidateItem]
    estimated_nutrition: MealAnalysisNutrition
    explanation: str
    warnings: list[str]
