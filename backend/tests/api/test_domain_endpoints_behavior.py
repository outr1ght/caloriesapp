import re
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.db.models.domain_enums import MealPlanStatus, RecommendationStatus, RecommendationType
from app.services.meal_plan_service import MealPlanService
from app.services.recommendations_service import RecommendationsService
from app.services.weight_log_service import WeightLogService

UTC_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


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

    recommendations_response = client.get("/api/v1/recommendations?page=1&page_size=10")
    assert recommendations_response.status_code == 200
    recommendations_body = recommendations_response.json()
    assert recommendations_body["data"] == {
        "items": [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "status": "ready",
                "type": "daily_summary",
                "title": "Daily summary",
            }
        ],
        "meta": {
            "page": 1,
            "page_size": 10,
            "total": 1,
            "total_pages": 1,
        },
    }

    recommendation_update = client.patch(
        "/api/v1/recommendations/11111111-1111-1111-1111-111111111111/status",
        json={"status": "applied"},
    )
    assert recommendation_update.status_code == 200
    assert recommendation_update.json()["data"]["status"] == "ready"

    weights_response = client.get("/api/v1/weights?page=1&page_size=30")
    assert weights_response.status_code == 200
    weights_body = weights_response.json()
    assert weights_body["data"]["meta"] == {
        "page": 1,
        "page_size": 30,
        "total": 1,
        "total_pages": 1,
    }
    assert len(weights_body["data"]["items"]) == 1
    assert UTC_DATETIME_RE.fullmatch(weights_body["data"]["items"][0]["logged_at"])

    plans_response = client.get("/api/v1/meal-plans")
    assert plans_response.status_code == 200
    assert len(plans_response.json()["data"]["items"]) == 1
    assert plans_response.json()["data"]["items"][0]["status"] == "active"
    assert UTC_DATETIME_RE.fullmatch(plans_response.json()["data"]["items"][0]["plan_date"])


@pytest.mark.usefixtures("auth_overrides")
def test_recommendations_empty_list_uses_canonical_pagination_shape(client, monkeypatch):
    async def _list_recommendations(self, user_id, page, page_size, status, recommendation_type):
        _ = (self, user_id, page, page_size, status, recommendation_type)
        return [], 0

    monkeypatch.setattr(RecommendationsService, "list", _list_recommendations)

    response = client.get("/api/v1/recommendations?page=2&page_size=5")
    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "meta": {
            "page": 2,
            "page_size": 5,
            "total": 0,
            "total_pages": 0,
        },
    }


@pytest.mark.usefixtures("auth_overrides")
def test_recommendation_and_meal_plan_negative_paths(client, monkeypatch):
    async def _missing_recommendation(self, user_id, recommendation_id, status):
        _ = (self, user_id, recommendation_id, status)
        raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.recommendations.not_found", status_code=404)

    async def _missing_plan(self, user_id, plan_id, payload):
        _ = (self, user_id, plan_id, payload)
        raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meal_plans.not_found", status_code=404)

    monkeypatch.setattr(RecommendationsService, "set_status", _missing_recommendation)
    monkeypatch.setattr(MealPlanService, "update", _missing_plan)

    invalid_recommendation_id = client.patch("/api/v1/recommendations/not-a-uuid/status", json={"status": "applied"})
    assert invalid_recommendation_id.status_code == 422

    missing_recommendation = client.patch(
        "/api/v1/recommendations/11111111-1111-1111-1111-111111111111/status",
        json={"status": "applied"},
    )
    assert missing_recommendation.status_code == 404

    invalid_plan_payload = client.post("/api/v1/meal-plans", json={})
    assert invalid_plan_payload.status_code == 422

    missing_plan = client.patch(
        "/api/v1/meal-plans/33333333-3333-3333-3333-333333333333",
        json={"title": "Updated"},
    )
    assert missing_plan.status_code == 404
