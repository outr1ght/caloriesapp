from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, SecretStr

from app.db.models.enums import AuthProvider, LanguageCode, UserRole

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(min_length=3, max_length=320, pattern=EMAIL_PATTERN)
    password: SecretStr = Field(min_length=8, max_length=128)
    locale: LanguageCode = LanguageCode.EN
    timezone: str = Field(default="UTC", min_length=1, max_length=64)


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(min_length=3, max_length=320, pattern=EMAIL_PATTERN)
    password: SecretStr = Field(min_length=8, max_length=128)


class RefreshTokenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    refresh_token: str = Field(..., min_length=32, max_length=4096)


class OAuthLoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: AuthProvider
    code: str | None = Field(default=None, min_length=1, max_length=4096)
    id_token: str | None = Field(default=None, min_length=1, max_length=8192)
    redirect_uri: str | None = Field(default=None, min_length=1, max_length=2048)


class LogoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    refresh_token: str | None = Field(default=None, min_length=32, max_length=4096)


class TokenPairDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    access_token: str = Field(..., min_length=1, max_length=8192)
    refresh_token: str = Field(..., min_length=32, max_length=4096)
    token_type: str = "bearer"
    expires_in: int


class AuthUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    id: str
    email: str = Field(min_length=3, max_length=320, pattern=EMAIL_PATTERN)
    role: UserRole
    locale: LanguageCode
    timezone: str
    is_active: bool
    is_verified: bool
    created_at: datetime


class AuthSessionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user: AuthUserDTO
    tokens: TokenPairDTO
