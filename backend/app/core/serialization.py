from datetime import UTC, date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel


def format_datetime_utc(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    else:
        value = value.astimezone(UTC)
    return value.isoformat().replace("+00:00", "Z")


def serialize_api_data(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return serialize_api_data(value.model_dump(mode="python"))
    if isinstance(value, datetime):
        return format_datetime_utc(value)
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: serialize_api_data(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [serialize_api_data(item) for item in value]
    return value
