from datetime import UTC, datetime

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.db.models.domain_enums import MealType, MealSource
from app.services.meal_service import MealService


@pytest.mark.usefixtures("auth_overrides")
def test_validation_errors_use_normalized_contract(client):
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
    assert body == {
        "ok": False,
        "message_key": "errors.validation.invalid_request",
        "data": None,
        "error": body["error"],
        "meta": {},
    }
    assert body["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "fields" in body["error"]["details"]


@pytest.mark.usefixtures("auth_overrides")
def test_app_exceptions_use_normalized_contract(client, monkeypatch):
    async def _not_found(self, user_id, meal_id):
        _ = (self, user_id, meal_id)
        raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meals.not_found", status_code=404)

    monkeypatch.setattr(MealService, "get_meal", _not_found)

    response = client.get("/api/v1/meals/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    assert response.status_code == 404
    assert response.json() == {
        "ok": False,
        "message_key": "errors.meals.not_found",
        "data": None,
        "error": {"code": ErrorCode.NOT_FOUND.value, "details": {}},
        "meta": {},
    }
