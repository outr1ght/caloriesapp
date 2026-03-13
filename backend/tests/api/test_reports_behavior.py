import pytest

from app.schemas.reports import NutritionReportDTO
from app.services.report_service import ReportService


@pytest.mark.usefixtures("auth_overrides")
def test_reports_empty_result_shape(client, monkeypatch):
    async def _nutrition_report(self, user_id, date_from, date_to):
        _ = (self, user_id, date_from, date_to)
        return NutritionReportDTO(
            date_from=date_from,
            date_to=date_to,
            totals_calories=0,
            avg_daily_calories=0,
            days=[],
        )

    monkeypatch.setattr(ReportService, "nutrition_report", _nutrition_report)

    response = client.get("/api/v1/reports/nutrition?date_from=2026-03-01&date_to=2026-03-01")
    assert response.status_code == 200
    assert response.json()["data"]["days"] == []


@pytest.mark.usefixtures("auth_overrides")
def test_reports_invalid_date_range(client):
    response = client.get("/api/v1/reports/nutrition?date_from=2026-03-05&date_to=2026-03-01")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
