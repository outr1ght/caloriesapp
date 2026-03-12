from decimal import Decimal
import pytest

@pytest.fixture
def sample_user_id() -> str:
    return "11111111-1111-1111-1111-111111111111"

@pytest.fixture
def sample_nutrition_payload() -> dict:
    return {"calories": Decimal("250.00"), "protein_g": Decimal("20.00"), "carbs_g": Decimal("15.00"), "fat_g": Decimal("10.00"), "fiber_g": Decimal("3.00"), "sugar_g": Decimal("2.00"), "sodium_mg": Decimal("180.00")}
