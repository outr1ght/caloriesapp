from datetime import UTC, datetime
from decimal import Decimal
from app.schemas.meals import MealCreateRequest, MealItemCreateRequest, NutritionValueDTO

def meal_create_request_factory() -> MealCreateRequest:
    return MealCreateRequest(title="Chicken and rice", meal_type="lunch", eaten_at=datetime.now(UTC), items=[MealItemCreateRequest(display_name="Chicken breast", quantity=Decimal("150"), unit="g", position=0, nutrition=NutritionValueDTO(calories=Decimal("250"), protein_g=Decimal("30"), carbs_g=Decimal("0"), fat_g=Decimal("6"), fiber_g=Decimal("0"), sugar_g=Decimal("0"), sodium_mg=Decimal("120")))])
