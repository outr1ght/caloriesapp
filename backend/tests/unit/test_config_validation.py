import pytest
from pydantic import ValidationError

from app.core.config import Settings


BASE_CONFIG = {
    "database_url": "postgresql+asyncpg://postgres:postgres@localhost:5432/nutrition_app_test",
}


def test_invalid_env_rejected():
    with pytest.raises(ValidationError) as exc:
        Settings(**BASE_CONFIG, env="staging")
    assert "Input should be 'development', 'test' or 'production'" in str(exc.value)


def test_development_config_allows_missing_secret():
    settings = Settings(**BASE_CONFIG, env="development", secret_key=None, openai_enabled=False, uploads_enabled=False)
    assert settings.secret_key == "dev-secret-key-dev-secret-key-123456"


def test_production_placeholder_secret_rejected():
    with pytest.raises(ValidationError) as exc:
        Settings(
            **BASE_CONFIG,
            env="production",
            secret_key="change-this-to-a-long-random-secret-change-this",
            debug=False,
            openai_enabled=False,
            uploads_enabled=False,
        )
    assert "APP_SECRET_KEY is unsafe for production" in str(exc.value)


def test_production_debug_true_rejected():
    with pytest.raises(ValidationError) as exc:
        Settings(
            **BASE_CONFIG,
            env="production",
            secret_key="this-is-a-strong-production-secret-key-1234567890",
            debug=True,
            openai_enabled=False,
            uploads_enabled=False,
        )
    assert "APP_DEBUG must be false" in str(exc.value)


def test_production_openai_enabled_requires_key():
    with pytest.raises(ValidationError) as exc:
        Settings(
            **BASE_CONFIG,
            env="production",
            secret_key="this-is-a-strong-production-secret-key-1234567890",
            debug=False,
            openai_enabled=True,
            openai_api_key="",
            uploads_enabled=False,
        )
    assert "APP_OPENAI_API_KEY must be set" in str(exc.value)


def test_production_uploads_enabled_requires_s3_credentials():
    with pytest.raises(ValidationError) as exc:
        Settings(
            **BASE_CONFIG,
            env="production",
            secret_key="this-is-a-strong-production-secret-key-1234567890",
            debug=False,
            openai_enabled=False,
            uploads_enabled=True,
            s3_bucket="nutrition-assets",
            s3_access_key_id="",
            s3_secret_access_key="",
        )
    assert "Production uploads require non-empty S3 configuration" in str(exc.value)


def test_production_safe_config_passes():
    settings = Settings(
        **BASE_CONFIG,
        env="production",
        secret_key="this-is-a-strong-production-secret-key-1234567890",
        debug=False,
        openai_enabled=True,
        openai_api_key="sk-test-key",
        uploads_enabled=True,
        s3_bucket="nutrition-assets",
        s3_access_key_id="access-key",
        s3_secret_access_key="secret-key-value",
    )
    assert settings.env == "production"
