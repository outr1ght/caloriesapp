from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.db.models.domain_enums import MealSource, MealType, UploadStatus
from app.services.meal_service import MealService


@pytest.mark.usefixtures("auth_overrides")
def test_meal_crud_and_ownership_checks(client, monkeypatch, sample_user):
    now = datetime.now(UTC)
    meal = SimpleNamespace(
        id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        user_id=sample_user.id,
        title="Chicken bowl",
        notes=None,
        meal_type=MealType.LUNCH,
        source=MealSource.MANUAL,
        eaten_at=now,
        analysis_status="ready",
        nutrition_value_id=None,
        metadata_json=None,
        created_at=now,
        updated_at=now,
        deleted_at=None,
        items=[
            SimpleNamespace(
                id="cccccccc-cccc-cccc-cccc-cccccccccccc",
                ingredient_id=None,
                food_product_id=None,
                display_name="Chicken breast",
                quantity=Decimal("150"),
                unit="g",
                position=0,
            )
        ],
        nutrition_value=SimpleNamespace(
            calories=Decimal("320"),
            protein_g=Decimal("35"),
            carbs_g=Decimal("12"),
            fat_g=Decimal("9"),
        ),
        uploaded_images=[
            SimpleNamespace(
                id="dddddddd-dddd-dddd-dddd-dddddddddddd",
                storage_key="uploads/user/meal-photo.jpg",
                mime_type="image/jpeg",
                file_size=12345,
                status=UploadStatus.UPLOADED,
                created_at=now,
            )
        ],
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
    assert set(create_response.json()) == {"ok", "message_key", "data", "error", "meta"}

    list_response = client.get("/api/v1/meals?page=2&page_size=1")
    assert list_response.status_code == 200
    list_body = list_response.json()
    assert set(list_body["data"]) == {"items", "meta"}
    assert list_body["data"]["meta"] == {
        "page": 2,
        "page_size": 1,
        "total": 1,
        "total_pages": 1,
    }
    assert set(list_body["data"]["items"][0]) == {
        "id",
        "user_id",
        "title",
        "notes",
        "meal_type",
        "source",
        "eaten_at",
        "analysis_status",
        "nutrition_summary",
        "items",
        "images",
        "created_at",
        "updated_at",
    }
    assert list_body["data"]["items"][0]["nutrition_summary"] == {
        "calories": "320",
        "protein_g": "35",
        "carbs_g": "12",
        "fat_g": "9",
    }
    assert list_body["data"]["items"][0]["items"] == [
        {
            "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "ingredient_id": None,
            "food_product_id": None,
            "display_name": "Chicken breast",
            "quantity": "150",
            "unit": "g",
            "position": 0,
        }
    ]
    assert list_body["data"]["items"][0]["images"] == [
        {
            "id": "dddddddd-dddd-dddd-dddd-dddddddddddd",
            "storage_key": "uploads/user/meal-photo.jpg",
            "mime_type": "image/jpeg",
            "file_size": 12345,
            "status": "uploaded",
            "created_at": now.isoformat().replace("+00:00", "Z"),
        }
    ]

    get_response = client.get(f"/api/v1/meals/{meal.id}")
    assert get_response.status_code == 200
    get_body = get_response.json()
    assert get_body["data"]["id"] == meal.id
    assert get_body["data"]["nutrition_summary"]["calories"] == "320"
    assert len(get_body["data"]["items"]) == 1
    assert len(get_body["data"]["images"]) == 1

    update_response = client.patch(f"/api/v1/meals/{meal.id}", json={"title": "Updated"})
    assert update_response.status_code == 200

    delete_response = client.delete(f"/api/v1/meals/{meal.id}")
    assert delete_response.status_code == 200


@pytest.mark.usefixtures("auth_overrides")
def test_meal_list_empty_shape_and_meta(client, monkeypatch):
    async def _list(self, user_id, query):
        _ = (self, user_id, query)
        return [], 0

    monkeypatch.setattr(MealService, "list_meals", _list)

    response = client.get("/api/v1/meals?page=1&page_size=20")
    assert response.status_code == 200
    body = response.json()
    assert body["data"] == {
        "items": [],
        "meta": {
            "page": 1,
            "page_size": 20,
            "total": 0,
            "total_pages": 0,
        },
    }


@pytest.mark.usefixtures("auth_overrides")
def test_meal_not_found_and_ownership_errors(client, monkeypatch):
    async def _not_found(self, user_id, meal_id):
        _ = (self, user_id, meal_id)
        raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meals.not_found", status_code=404)

    async def _update_not_found(self, user_id, meal_id, payload):
        _ = (self, user_id, meal_id, payload)
        raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meals.not_found", status_code=404)

    async def _delete_not_found(self, user_id, meal_id):
        _ = (self, user_id, meal_id)
        raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meals.not_found", status_code=404)

    monkeypatch.setattr(MealService, "get_meal", _not_found)
    monkeypatch.setattr(MealService, "update_meal", _update_not_found)
    monkeypatch.setattr(MealService, "delete_meal", _delete_not_found)

    get_response = client.get("/api/v1/meals/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    assert get_response.status_code == 404
    assert get_response.json()["error"]["code"] == ErrorCode.NOT_FOUND.value

    update_response = client.patch("/api/v1/meals/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", json={"title": "Updated"})
    assert update_response.status_code == 404

    delete_response = client.delete("/api/v1/meals/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    assert delete_response.status_code == 404


@pytest.mark.usefixtures("auth_overrides")
def test_meal_invalid_payload_rejected(client):
    response = client.post(
        "/api/v1/meals",
        json={
            "title": "Invalid meal",
            "meal_type": "lunch",
            "source": "manual",
            "eaten_at": datetime.now(UTC).isoformat(),
            "items": [],
        },
    )
    assert response.status_code == 422
    body = response.json()
    assert body["ok"] is False
    assert body["message_key"] == "errors.validation.invalid_request"
    assert body["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


@pytest.mark.usefixtures("auth_overrides")
def test_meal_invalid_uuid_rejected(client):
    response = client.get("/api/v1/meals/not-a-uuid")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_meal_openapi_exposes_explicit_read_schemas(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()

    list_schema_ref = schema["paths"]["/api/v1/meals"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    detail_schema_ref = schema["paths"]["/api/v1/meals/{meal_id}"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]

    assert list_schema_ref.endswith("/MealListEnvelopeResponse")
    assert detail_schema_ref.endswith("/MealReadEnvelopeResponse")
    assert "MealReadResponse" in schema["components"]["schemas"]
    assert "MealListDataResponse" in schema["components"]["schemas"]
