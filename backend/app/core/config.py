from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    app_name: str = "CaloriesApp API"
    api_v1_prefix: str = "/api/v1"

    jwt_secret_key: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 15
    refresh_token_expires_days: int = 30

    database_url: str
    redis_url: str

    s3_endpoint_url: str | None = None
    s3_bucket: str = "calories-images"
    s3_access_key: str | None = None
    s3_secret_key: str | None = None

    openai_api_key: str | None = None
    openai_model_vision: str = "gpt-4.1-mini"
    openai_model_text: str = "gpt-4.1-mini"

    max_upload_mb: int = 8
    allowed_image_mime: str = "image/jpeg,image/png,image/webp"

    sentry_dsn: str | None = None


settings = Settings()
