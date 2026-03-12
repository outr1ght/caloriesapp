from pydantic import BaseModel, ConfigDict, Field


class BarcodeLookupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(min_length=4, max_length=64)


class BarcodeLookupResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    found: bool
    product: dict | None = None
