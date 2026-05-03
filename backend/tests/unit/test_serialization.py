from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from app.core.serialization import format_datetime_utc, serialize_api_data


class DemoEnum(StrEnum):
    READY = "ready"


def test_format_datetime_utc_uses_z_suffix() -> None:
    value = datetime(2026, 5, 2, 12, 34, 56, tzinfo=UTC)
    assert format_datetime_utc(value) == "2026-05-02T12:34:56Z"


def test_serialize_api_data_normalizes_datetime_enum_and_decimal() -> None:
    data = {
        "created_at": datetime(2026, 5, 2, 12, 34, 56, tzinfo=UTC),
        "status": DemoEnum.READY,
        "amount": Decimal("12.5"),
        "nested": [datetime(2026, 5, 2, 13, 0, 0, tzinfo=UTC)],
    }

    assert serialize_api_data(data) == {
        "created_at": "2026-05-02T12:34:56Z",
        "status": "ready",
        "amount": "12.5",
        "nested": ["2026-05-02T13:00:00Z"],
    }
