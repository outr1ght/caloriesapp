from datetime import UTC, datetime
from decimal import Decimal
from app.schemas.goals import NutritionGoalCreateRequest, NutritionGoalUpdateRequest

def test_goal_create_payload() -> None:
    payload = NutritionGoalCreateRequest(strategy="maintain", activity_level="moderate", target_calories=Decimal("2200"), effective_from=datetime.now(UTC))
    assert payload.target_calories == Decimal("2200")

def test_goal_update_payload_partial() -> None:
    assert NutritionGoalUpdateRequest(target_calories=Decimal("2100"), is_active=False).is_active is False
