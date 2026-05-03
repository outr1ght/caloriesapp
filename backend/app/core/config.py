from functools import lru_cache
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_ALLOWED_ENVS = ("development", "test", "production")
_DEFAULT_DEV_SECRET = "dev-secret-key-dev-secret-key-123456"
_PLACEHOLDER_SECRETS = {
    "change-this-to-a-long-random-secret-change-this",
    "test-secret-key-test-secret-key-123456",
    "dev-secret-key-dev-secret-key-123456",
    "changemechangemechangemechangeme1234",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
        case_sensitive=False,
    )

    env: Literal["development", "test", "production"] = "development"
    debug: bool = False
    project_name: str = "Nutrition Assistant API"
    api_v1_prefix: str = "/api/v1"
    secret_key: str | None = None
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    database_url: str
    database_echo: bool = False
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = Field(default_factory=list)

    google_oauth_client_id: str | None = None
    apple_oauth_client_id: str | None = None
    apple_oauth_jwks_url: str = "https://appleid.apple.com/auth/keys"

    openai_enabled: bool = True
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    openai_timeout_seconds: int = 20
    openai_max_retries: int = 2

    uploads_enabled: bool = True
    s3_endpoint_url: str | None = None
    s3_region: str = "us-east-1"
    s3_bucket: str = "nutrition-assets"
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    s3_use_ssl: bool = True

    max_upload_bytes: int = 5 * 1024 * 1024
    allowed_upload_mime: list[str] = Field(default_factory=lambda: ["image/jpeg", "image/png", "image/webp"])

    rate_limit_per_minute: int = 120
    rate_limit_auth_per_minute: int | None = None
    rate_limit_meal_analysis_per_minute: int | None = None
    rate_limit_uploads_per_minute: int | None = None
    max_report_range_days: int = 93

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        raise ValueError("Invalid CORS origins value")

    @field_validator("allowed_upload_mime", mode="before")
    @classmethod
    def parse_allowed_mime(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip().lower() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip().lower() for item in value if str(item).strip()]
        raise ValueError("Invalid allowed upload mime value")

    @staticmethod
    def _is_weak_secret(value: str) -> bool:
        normalized = value.strip().lower()
        return (
            len(value) < 32
            or normalized in _PLACEHOLDER_SECRETS
            or "change-this" in normalized
            or len(set(value)) < 8
        )

    @model_validator(mode="after")
    def validate_runtime_safety(self) -> "Settings":
        if self.env in {"development", "test"}:
            if not self.secret_key:
                self.secret_key = _DEFAULT_DEV_SECRET
            return self

        if self.env != "production":
            raise ValueError(f"APP_ENV must be one of: {', '.join(_ALLOWED_ENVS)}")

        if not self.secret_key:
            raise ValueError("APP_SECRET_KEY must be set when APP_ENV=production")
        if self._is_weak_secret(self.secret_key):
            raise ValueError("APP_SECRET_KEY is unsafe for production; use a strong random secret")
        if self.debug:
            raise ValueError("APP_DEBUG must be false when APP_ENV=production")
        if self.openai_enabled and not (self.openai_api_key and self.openai_api_key.strip()):
            raise ValueError("APP_OPENAI_API_KEY must be set when APP_ENV=production and APP_OPENAI_ENABLED=true")
        if self.uploads_enabled:
            missing_fields = []
            if not self.s3_bucket.strip():
                missing_fields.append("APP_S3_BUCKET")
            if not (self.s3_access_key_id and self.s3_access_key_id.strip()):
                missing_fields.append("APP_S3_ACCESS_KEY_ID")
            if not (self.s3_secret_access_key and self.s3_secret_access_key.strip()):
                missing_fields.append("APP_S3_SECRET_ACCESS_KEY")
            if missing_fields:
                raise ValueError(
                    "Production uploads require non-empty S3 configuration: " + ", ".join(missing_fields)
                )
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
