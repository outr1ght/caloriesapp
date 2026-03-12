from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    id: str
    locale: str
    summary: str


class MealPlanResponse(BaseModel):
    id: str
    locale: str
    plan_json: str


class BarcodeScanRequest(BaseModel):
    code: str


class BarcodeScanResponse(BaseModel):
    found: bool
    product_name: str | None = None
    brand: str | None = None
    nutrition_per_100g: dict[str, float] | None = None
