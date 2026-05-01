import pytest

from app.common.exceptions import AppException
from app.services.meal_analysis_service import MealAnalysisService


@pytest.mark.asyncio
async def test_meal_analysis_requires_images() -> None:
    with pytest.raises(AppException):
        await MealAnalysisService().analyze("meal-1", [])


@pytest.mark.asyncio
async def test_meal_analysis_schema_mismatch_uses_fallback(monkeypatch) -> None:
    service = MealAnalysisService()

    async def _generate_json(*, prompt, schema):
        _ = (prompt, schema)
        return {"explanation": ["bad"], "warnings": "bad"}

    monkeypatch.setattr(service.openai, "generate_json", _generate_json)

    result = await service.analyze("meal-1", ["img-1"])
    assert result.warnings == ["openai_output_invalid"]
    assert "Estimated from visible portions" in result.explanation


@pytest.mark.asyncio
async def test_meal_analysis_openai_unavailable_uses_fallback(monkeypatch) -> None:
    service = MealAnalysisService()

    async def _generate_json(*, prompt, schema):
        _ = (prompt, schema)
        return {"text": "", "items": [], "warnings": ["openai_unavailable"]}

    monkeypatch.setattr(service.openai, "generate_json", _generate_json)

    result = await service.analyze("meal-1", ["img-1"])
    assert result.warnings == ["openai_unavailable"]
    assert "Estimated from visible portions" in result.explanation
