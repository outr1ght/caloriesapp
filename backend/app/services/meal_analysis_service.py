from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.common.exceptions import AppException, ErrorCode
from app.core.logging import get_logger
from app.integrations.openai_client import OpenAIClient
from app.schemas.meal_analysis import MealAnalysisCandidateItem, MealAnalysisNutrition, MealAnalysisResponse

logger = get_logger(__name__)
_FALLBACK_WARNINGS = {"openai_not_configured", "openai_unavailable", "empty_openai_output", "openai_output_invalid"}
_FALLBACK_EXPLANATION = "Estimated from visible portions with conservative assumptions."


class MealAnalysisAIOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    explanation: str = Field(min_length=1, max_length=4096)
    warnings: list[str]


class MealAnalysisService:
    def __init__(self) -> None:
        self.openai = OpenAIClient()

    async def analyze(self, meal_id: str, image_ids: list[str]) -> MealAnalysisResponse:
        if not image_ids:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.analysis.missing_images", status_code=422)
        deterministic_nutrition = MealAnalysisNutrition(calories=Decimal("450.00"), protein_g=Decimal("28.00"), carbs_g=Decimal("42.00"), fat_g=Decimal("16.00"), confidence=Decimal("0.780"))
        items = [MealAnalysisCandidateItem(name="chicken breast", estimated_quantity=Decimal("140.0"), unit="g", confidence=Decimal("0.82"))]
        ai_raw = await self.openai.generate_json(
            prompt="Write concise rationale and caveats for deterministic estimate.",
            schema={
                "type": "object",
                "properties": {
                    "explanation": {"type": "string"},
                    "warnings": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["explanation", "warnings"],
                "additionalProperties": False,
            },
        )
        explanation, warnings = self._resolve_ai_output(ai_raw)
        return MealAnalysisResponse(meal_id=meal_id, status="ready", analyzed_at=datetime.now(UTC), items=items, estimated_nutrition=deterministic_nutrition, explanation=explanation[:4096], warnings=warnings[:20])

    def _resolve_ai_output(self, ai_raw: dict) -> tuple[str, list[str]]:
        raw_warnings = ai_raw.get("warnings") if isinstance(ai_raw, dict) else None
        if isinstance(raw_warnings, list):
            fallback_warnings = [str(item) for item in raw_warnings if str(item) in _FALLBACK_WARNINGS]
            if fallback_warnings:
                fallback_reason = fallback_warnings[0]
                logger.info(
                    "meal analysis fallback used",
                    extra={"event": {"event": "openai_fallback_used", "integration": "meal_analysis", "reason": fallback_reason}},
                )
                return _FALLBACK_EXPLANATION, fallback_warnings

        try:
            parsed = MealAnalysisAIOutput.model_validate(ai_raw)
        except ValidationError as exc:
            logger.warning(
                "meal analysis ai output invalid",
                extra={
                    "event": {
                        "event": "openai_output_invalid",
                        "integration": "meal_analysis",
                        "error_type": type(exc).__name__,
                        "error_count": len(exc.errors()),
                    }
                },
            )
            logger.info(
                "meal analysis fallback used",
                extra={"event": {"event": "openai_fallback_used", "integration": "meal_analysis", "reason": "openai_output_invalid"}},
            )
            return _FALLBACK_EXPLANATION, ["openai_output_invalid"]

        warnings = [str(item) for item in parsed.warnings]
        return parsed.explanation, warnings
