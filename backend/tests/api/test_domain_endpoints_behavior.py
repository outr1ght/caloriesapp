from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from app.db.models.domain_enums import MealPlanStatus, RecommendationStatus, RecommendationType
from app.services.meal_plan_service import MealPlanService
from app.services.recommendations_service import RecommendationsService
from app.services.weight_log_service import WeightLogService


@pytest.mark.usefixtures("auth_overrides")
def test_recommendations_weights_meal_plans_basics(client, monkeypatch):
    recommendation = SimpleNamespace(
        id="11111111-1111-1111-1111-111111111111",
        status=RecommendationStatus.READY,
        recommendation_type=RecommendationType.DAILY_SUMMARY,
        title="Daily summary",
    )
    weight_log = SimpleNamespace(id="22222222-2222-2222-2222-222222222222", logged_at=datetime.now(UTC), weight_kg="80.2")
    meal_plan = SimpleNamespace(
        id="33333333-3333-3333-3333-333333333333",
        status=MealPlanStatus.ACTIVE,
        plan_date=datetime.now(UTC),
        title="Plan",
    )

    async def _list_recommendations(self, user_id, page, page_size, status, recommendation_type):
        _ = (self, user_id, page, page_size, status, recommendation_type)
        return [recommendation], 1

    async def _set_recommendation_status(self, user_id, recommendation_id, status):
        _ = (self, user_id, recommendation_id, status)
        return recommendation

    async def _list_weights(self, user_id, query):
        _ = (self, user_id, query)
        return [weight_log], 1

    async def _list_plans(self, user_id):
        _ = (self, user_id)
        return [meal_plan]

    monkeypatch.setattr(RecommendationsService, "list", _list_recommendations)
    monkeypatch.setattr(RecommendationsService, "set_status", _set_recommendation_status)
    monkeypatch.setattr(WeightLogService, "list", _list_weights)
    monkeypatch.setattr(MealPlanService, "list", _list_plans)

    recommendations_response = client.get("/api/v1/recommendations")
    assert recommendations_response.status_code == 200
    assert recommendations_response.json()["data"]["total"] == 1

    recommendation_update = client.patch(
        "/api/v1/recommendations/11111111-1111-1111-1111-111111111111/status",
        json={"status": "applied"},
    )
    assert recommendation_update.status_code == 200

    weights_response = client.get("/api/v1/weights")
    assert weights_response.status_code == 200
    assert weights_response.json()["data"]["total"] == 1

    plans_response = client.get("/api/v1/meal-plans")
    assert plans_response.status_code == 200
    assert len(plans_response.json()["data"]["items"]) == 1
