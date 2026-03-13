import pytest

from app.common.exceptions import AppException, ErrorCode
from app.services.meal_analysis_service import MealAnalysisService


class _AnalysisPayload:
    def model_dump(self):
        return {
            "meal_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "status": "ready",
            "items": [{"name": "rice", "estimated_quantity": "120", "unit": "g", "confidence": "0.6"}],
            "estimated_nutrition": {
                "calories": "180",
                "protein_g": "4",
                "carbs_g": "38",
                "fat_g": "1",
                "confidence": "0.6",
            },
            "explanation": "Low confidence estimate.",
            "warnings": ["low_confidence"],
            "analyzed_at": "2026-03-13T00:00:00Z",
        }


@pytest.mark.usefixtures("auth_overrides")
def test_meal_analysis_success_and_validation(client, monkeypatch):
    async def _analyze(self, meal_id, image_ids):
        _ = (self, meal_id, image_ids)
        return _AnalysisPayload()

    monkeypatch.setattr(MealAnalysisService, "analyze", _analyze)

    response = client.post(
        "/api/v1/meals/analysis",
        json={"meal_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "uploaded_image_ids": ["img-1"]},
    )
    assert response.status_code == 200
    assert response.json()["data"]["warnings"] == ["low_confidence"]

    invalid = client.post("/api/v1/meals/analysis", json={"meal_id": "not-a-uuid", "uploaded_image_ids": ["img-1"]})
    assert invalid.status_code == 422


@pytest.mark.usefixtures("auth_overrides")
def test_meal_analysis_error_path(client, monkeypatch):
    async def _analyze(self, meal_id, image_ids):
        _ = (self, meal_id, image_ids)
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.analysis.missing_images", status_code=422)

    monkeypatch.setattr(MealAnalysisService, "analyze", _analyze)
    response = client.post(
        "/api/v1/meals/analysis",
        json={"meal_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "uploaded_image_ids": []},
    )
    assert response.status_code == 422
