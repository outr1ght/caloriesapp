from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UploadInitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    filename: str = Field(min_length=1, max_length=255)
    mime_type: str = Field(min_length=3, max_length=128)
    file_size: int = Field(gt=0)
    sha256: str = Field(min_length=64, max_length=64)
    meal_id: str | None = None


class UploadCompleteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    upload_id: str


class UploadInitResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    upload_id: str
    storage_key: str
    upload_url: str
    upload_headers: dict[str, str]
    expires_at: datetime
