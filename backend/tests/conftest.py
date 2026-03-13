import os

os.environ.setdefault("APP_SECRET_KEY", "test-secret-key-test-secret-key-123456")
os.environ.setdefault("APP_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/nutrition_app_test")
os.environ.setdefault("APP_REDIS_URL", "redis://localhost:6379/15")
from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.db.models.domain_enums import ActivityLevel, GoalStrategy, MealSource, MealType, RecommendationStatus, RecommendationType
from app.db.models.enums import LanguageCode, UserRole
from app.main import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user() -> SimpleNamespace:
    return SimpleNamespace(
        id="11111111-1111-1111-1111-111111111111",
        email="user@example.com",
        role=UserRole.USER,
        locale=LanguageCode.EN,
        timezone="UTC",
        is_active=True,
        is_verified=False,
        created_at=datetime.now(UTC),
        deleted_at=None,
    )


@pytest.fixture
def auth_overrides(sample_user: SimpleNamespace):
    async def _get_user_override() -> SimpleNamespace:
        return sample_user

    async def _get_session_override():
        yield object()

    app.dependency_overrides[get_current_user] = _get_user_override
    app.dependency_overrides[get_session] = _get_session_override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_id() -> str:
    return "11111111-1111-1111-1111-111111111111"


@pytest.fixture
def sample_nutrition_payload() -> dict:
    return {
        "calories": Decimal("250.00"),
        "protein_g": Decimal("20.00"),
        "carbs_g": Decimal("15.00"),
        "fat_g": Decimal("10.00"),
        "fiber_g": Decimal("3.00"),
        "sugar_g": Decimal("2.00"),
        "sodium_mg": Decimal("180.00"),
    }


@pytest.fixture
def sample_goal_payload() -> dict:
    return {
        "strategy": GoalStrategy.MAINTAIN,
        "activity_level": ActivityLevel.MODERATE,
        "target_calories": Decimal("2200.00"),
    }


@pytest.fixture
def sample_meal_payload() -> dict:
    return {
        "title": "Chicken and rice",
        "meal_type": MealType.LUNCH,
        "source": MealSource.MANUAL,
        "notes": None,
        "items": [],
    }


@pytest.fixture
def sample_recommendation_payload() -> dict:
    return {
        "id": "22222222-2222-2222-2222-222222222222",
        "status": RecommendationStatus.READY,
        "recommendation_type": RecommendationType.DAILY_SUMMARY,
        "title": "Daily nutrition summary",
    }

