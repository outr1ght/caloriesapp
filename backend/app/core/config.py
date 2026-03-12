from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="APP_", extra="ignore", case_sensitive=False)

    env: str = "development"
    debug: bool = False
    project_name: str = "Nutrition Assistant API"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    database_url: str
    database_echo: bool = False
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = Field(default_factory=list)
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    s3_endpoint_url: str | None = None
    s3_region: str = "us-east-1"
    s3_bucket: str = "nutrition-assets"
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    s3_use_ssl: bool = True
    max_upload_bytes: int = 5 * 1024 * 1024
    allowed_upload_mime: list[str] = Field(default_factory=lambda: ["image/jpeg", "image/png", "image/webp"])
    rate_limit_per_minute: int = 120

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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
