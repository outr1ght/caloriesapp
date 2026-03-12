from uuid import uuid4

from app.schemas.meal import MealAnalysisRequest, MealAnalysisResponse, MealItemIn, NutritionTotals
from app.services.ai.contracts import VisionAnalysis


class MealAnalysisService:
    def _fallback_analysis(self) -> VisionAnalysis:
        return VisionAnalysis(
            dish_name="mixed meal",
            analysis_confidence=0.62,
            items=[
                {"name": "chicken breast", "grams": 150, "confidence": 0.68},
                {"name": "rice", "grams": 120, "confidence": 0.63},
                {"name": "vegetables", "grams": 90, "confidence": 0.55},
            ],
        )

    def analyze(self, req: MealAnalysisRequest) -> MealAnalysisResponse:
        validated = self._fallback_analysis()

        items = [MealItemIn(name=i.name, grams=i.grams, confidence=i.confidence) for i in validated.items]
        nutrition = NutritionTotals(calories=520, protein_g=44, fat_g=13, carbs_g=56)
        confidence = validated.analysis_confidence
        return MealAnalysisResponse(
            analysis_id=str(uuid4()),
            analysis_confidence=confidence,
            requires_manual_review=confidence < 0.65,
            items=items,
            nutrition=nutrition,
        )


meal_analysis_service = MealAnalysisService()
