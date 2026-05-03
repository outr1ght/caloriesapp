import re
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from app.db.models.domain_enums import ActivityLevel, GoalStrategy
from app.db.models.enums import LanguageCode
from app.services.goals_service import GoalsService
from app.services.user_service import UserService

UTC_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


@pytest.mark.usefixtures("auth_overrides")
def test_profile_update_flow(client, monkeypatch, sample_user):
    now = datetime.now(UTC)
    profile = SimpleNamespace(
        id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        user_id=sample_user.id,
        first_name="Alex",
        last_name=None,
        birth_year=1990,
        gender="male",
        height_cm=180.0,
        created_at=now,
        updated_at=now,
    )

    async def _update_profile(self, user_id, payload):
        _ = (self, user_id, payload)
        return profile

    async def _update_locale(self, user_id, payload):
        _ = (self, user_id, payload)
        sample_user.locale = LanguageCode.ES
        sample_user.timezone = "Europe/Madrid"
        return sample_user

    monkeypatch.setattr(UserService, "update_profile", _update_profile)
    monkeypatch.setattr(UserService, "update_locale", _update_locale)

    profile_response = client.patch("/api/v1/me/profile", json={"first_name": "Alex", "height_cm": 180})
    assert profile_response.status_code == 200
    profile_body = profile_response.json()["data"]
    assert profile_body["first_name"] == "Alex"
    assert UTC_DATETIME_RE.fullmatch(profile_body["created_at"])
    assert UTC_DATETIME_RE.fullmatch(profile_body["updated_at"])

    locale_response = client.patch("/api/v1/me/locale", json={"locale": "es", "timezone": "Europe/Madrid"})
    assert locale_response.status_code == 200
    assert locale_response.json()["data"]["locale"] == "es"


@pytest.mark.usefixtures("auth_overrides")
def test_goals_update_flow(client, monkeypatch, sample_user):
    now = datetime.now(UTC)
    goal = SimpleNamespace(
        id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        user_id=sample_user.id,
        strategy=GoalStrategy.MAINTAIN,
        activity_level=ActivityLevel.MODERATE,
        target_calories=2200,
        target_protein_g=None,
        target_carbs_g=None,
        target_fat_g=None,
        target_water_ml=None,
        is_active=True,
        effective_from=now,
        effective_to=None,
        created_at=now,
        updated_at=now,
    )

    async def _active(self, user_id):
        _ = (self, user_id)
        return goal

    async def _create(self, user_id, payload):
        _ = (self, user_id, payload)
        return goal

    async def _update(self, user_id, goal_id, payload):
        _ = (self, user_id, goal_id, payload)
        return goal

    monkeypatch.setattr(GoalsService, "get_active_goal", _active)
    monkeypatch.setattr(GoalsService, "create_goal", _create)
    monkeypatch.setattr(GoalsService, "update_goal", _update)

    active_response = client.get("/api/v1/goals/active")
    assert active_response.status_code == 200
    active_body = active_response.json()["data"]
    assert active_body["strategy"] == "maintain"
    assert active_body["activity_level"] == "moderate"
    assert UTC_DATETIME_RE.fullmatch(active_body["effective_from"])
    assert UTC_DATETIME_RE.fullmatch(active_body["created_at"])
    assert UTC_DATETIME_RE.fullmatch(active_body["updated_at"])

    create_response = client.post(
        "/api/v1/goals",
        json={
            "strategy": "maintain",
            "activity_level": "moderate",
            "target_calories": 2200,
            "effective_from": datetime.now(UTC).isoformat(),
        },
    )
    assert create_response.status_code == 200

    update_response = client.patch(
        "/api/v1/goals/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        json={"target_calories": 2100, "is_active": True},
    )
    assert update_response.status_code == 200
