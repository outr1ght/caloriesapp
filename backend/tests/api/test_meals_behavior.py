from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.db.models.domain_enums import MealSource, MealType
from app.services.meal_service import MealService


@pytest.mark.usefixtures("auth_overrides")
def test_meal_crud_and_ownership_checks(client, monkeypatch, sample_user):
    meal = SimpleNamespace(
        id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        user_id=sample_user.id,
        title="Chicken bowl",
        notes=None,
        meal_type=MealType.LUNCH,
        source=MealSource.MANUAL,
        eaten_at=datetime.now(UTC),
        analysis_status="ready",
        nutrition_value_id=None,
        metadata_json=None,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        deleted_at=None,
        items=[],
        nutrition_value=None,
        uploaded_images=[],
    )

    async def _create(self, user_id, payload):
        _ = (self, user_id, payload)
        return meal

    async def _list(self, user_id, query):
        _ = (self, user_id, query)
        return [meal], 1

    async def _get(self, user_id, meal_id):
        _ = (self, user_id, meal_id)
        return meal

    async def _update(self, user_id, meal_id, payload):
        _ = (self, user_id, meal_id, payload)
        return meal

    async def _delete(self, user_id, meal_id):
        _ = (self, user_id, meal_id)
        return None

    monkeypatch.setattr(MealService, "create_meal", _create)
    monkeypatch.setattr(MealService, "list_meals", _list)
    monkeypatch.setattr(MealService, "get_meal", _get)
    monkeypatch.setattr(MealService, "update_meal", _update)
    monkeypatch.setattr(MealService, "delete_meal", _delete)

    create_response = client.post(
        "/api/v1/meals",
        json={
            "title": "Chicken bowl",
            "meal_type": "lunch",
            "source": "manual",
            "eaten_at": datetime.now(UTC).isoformat(),
            "items": [
                {
                    "display_name": "Chicken",
                    "quantity": "100",
                    "unit": "g",
                    "position": 0,
                    "nutrition": {
                        "calories": "200",
                        "protein_g": "25",
                        "carbs_g": "0",
                        "fat_g": "8",
                        "fiber_g": "0",
                        "sugar_g": "0",
                        "sodium_mg": "50",
                    },
                }
            ],
        },
    )
    assert create_response.status_code == 200

    list_response = client.get("/api/v1/meals")
    assert list_response.status_code == 200
    assert list_response.json()["data"]["total"] == 1

    get_response = client.get(f"/api/v1/meals/{meal.id}")
    assert get_response.status_code == 200

    update_response = client.patch(f"/api/v1/meals/{meal.id}", json={"title": "Updated"})
    assert update_response.status_code == 200

    delete_response = client.delete(f"/api/v1/meals/{meal.id}")
    assert delete_response.status_code == 200

    async def _get_denied(self, user_id, meal_id):
        _ = (self, user_id, meal_id)
        raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meals.not_found", status_code=404)

    monkeypatch.setattr(MealService, "get_meal", _get_denied)
    denied_response = client.get("/api/v1/meals/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    assert denied_response.status_code == 404


@pytest.mark.usefixtures("auth_overrides")
def test_meal_invalid_uuid_rejected(client):
    response = client.get("/api/v1/meals/not-a-uuid")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
