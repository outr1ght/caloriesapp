from decimal import Decimal
from app.schemas.meals import NutritionValueDTO
from app.services.nutrition_calculation_service import NutritionCalculationService

def test_nutrition_aggregate_sum() -> None:
    result = NutritionCalculationService.aggregate([
        NutritionValueDTO(calories=Decimal("100"), protein_g=Decimal("10"), carbs_g=Decimal("5"), fat_g=Decimal("2"), fiber_g=Decimal("1"), sugar_g=Decimal("1"), sodium_mg=Decimal("50")),
        NutritionValueDTO(calories=Decimal("150"), protein_g=Decimal("12"), carbs_g=Decimal("20"), fat_g=Decimal("3"), fiber_g=Decimal("2"), sugar_g=Decimal("3"), sodium_mg=Decimal("80")),
    ])
    assert result.calories == Decimal("250.00")
