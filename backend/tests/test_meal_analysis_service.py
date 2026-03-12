import pytest
from app.common.exceptions import AppException
from app.services.meal_analysis_service import MealAnalysisService

@pytest.mark.asyncio
async def test_meal_analysis_requires_images() -> None:
    with pytest.raises(AppException):
        await MealAnalysisService().analyze("meal-1", [])
