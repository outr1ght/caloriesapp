from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class WeightLogCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    logged_at: datetime
    weight_kg: Decimal = Field(gt=0)
    body_fat_percent: Decimal | None = Field(default=None, ge=0, le=100)
    note: str | None = Field(default=None, max_length=512)


class WeightLogUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    weight_kg: Decimal | None = Field(default=None, gt=0)
    body_fat_percent: Decimal | None = Field(default=None, ge=0, le=100)
    note: str | None = Field(default=None, max_length=512)


class WeightLogListQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")
    from_dt: datetime | None = None
    to_dt: datetime | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=30, ge=1, le=200)
