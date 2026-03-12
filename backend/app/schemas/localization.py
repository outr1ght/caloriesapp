from pydantic import BaseModel, ConfigDict, Field

from app.db.models.enums import LanguageCode


class MessageLookupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    keys: list[str] = Field(min_length=1, max_length=200)


class SupportedLocaleDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: LanguageCode
    label: str
