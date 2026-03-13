from pydantic import BaseModel, ConfigDict, Field


class BarcodeLookupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(min_length=8, max_length=32, pattern="^[0-9A-Za-z-]+$")


class BarcodeLookupResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    found: bool
    product: dict | None = None

