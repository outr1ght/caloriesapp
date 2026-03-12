from datetime import date
from app.schemas.reports import NutritionReportDTO

def test_report_schema_instantiation() -> None:
    payload = NutritionReportDTO(date_from=date(2026, 1, 1), date_to=date(2026, 1, 31), totals_calories=0, avg_daily_calories=0, days=[])
    assert payload.date_from < payload.date_to
