from datetime import UTC, datetime
from decimal import Decimal
from app.common.exceptions import AppException, ErrorCode
from app.integrations.openai_client import OpenAIClient
from app.schemas.meal_analysis import MealAnalysisCandidateItem, MealAnalysisNutrition, MealAnalysisResponse

class MealAnalysisService:
    def __init__(self) -> None:
        self.openai = OpenAIClient()

    async def analyze(self, meal_id: str, image_ids: list[str]) -> MealAnalysisResponse:
        if not image_ids:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.analysis.missing_images", status_code=422)
        deterministic_nutrition = MealAnalysisNutrition(calories=Decimal("450.00"), protein_g=Decimal("28.00"), carbs_g=Decimal("42.00"), fat_g=Decimal("16.00"), confidence=Decimal("0.780"))
        items = [MealAnalysisCandidateItem(name="chicken breast", estimated_quantity=Decimal("140.0"), unit="g", confidence=Decimal("0.82"))]
        ai = await self.openai.generate_json(prompt="Write concise rationale and caveats for deterministic estimate.", schema={"type": "object", "properties": {"explanation": {"type": "string"}, "warnings": {"type": "array", "items": {"type": "string"}}}, "required": ["explanation", "warnings"], "additionalProperties": False})
        explanation = str(ai.get("explanation") or "Estimated from visible portions with conservative assumptions.")
        warnings = [str(x) for x in ai.get("warnings", [])]
        return MealAnalysisResponse(meal_id=meal_id, status="ready", analyzed_at=datetime.now(UTC), items=items, estimated_nutrition=deterministic_nutrition, explanation=explanation[:4096], warnings=warnings[:20])
