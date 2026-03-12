from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.db.models.enums import LanguageCode, UserRole


class UserProfileDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    id: str
    user_id: str
    first_name: str | None = None
    last_name: str | None = None
    birth_year: int | None = None
    gender: str | None = None
    height_cm: float | None = None
    created_at: datetime
    updated_at: datetime


class UserProfileUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    birth_year: int | None = Field(default=None, ge=1900, le=2100)
    gender: str | None = Field(default=None, min_length=1, max_length=32)
    height_cm: float | None = Field(default=None, gt=30, lt=300)


class MeDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    email: EmailStr
    role: UserRole
    locale: LanguageCode
    timezone: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    profile: UserProfileDTO | None = None


class LocaleUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    locale: LanguageCode
    timezone: str = Field(min_length=1, max_length=64)
