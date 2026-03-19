from datetime import date, timedelta

import pytest

from app.common.exceptions import AppException
from app.services.report_service import ReportService


class _Session:
    async def execute(self, stmt):
        _ = stmt
        raise AssertionError("execute should not be called for invalid date ranges")


@pytest.mark.asyncio
async def test_report_invalid_range_rejected_before_query():
    service = ReportService(_Session())
    with pytest.raises(AppException) as exc:
        await service.nutrition_report("user-1", date(2026, 3, 10), date(2026, 3, 1))
    assert exc.value.status_code == 422
    assert exc.value.message_key == "errors.reports.invalid_date_range"


@pytest.mark.asyncio
async def test_report_range_too_large_rejected_before_query(monkeypatch: pytest.MonkeyPatch):
    service = ReportService(_Session())
    monkeypatch.setattr(service.settings, "max_report_range_days", 7)

    with pytest.raises(AppException) as exc:
        await service.nutrition_report("user-1", date(2026, 3, 1), date(2026, 3, 15))

    assert exc.value.status_code == 422
    assert exc.value.message_key == "errors.reports.range_too_large"
