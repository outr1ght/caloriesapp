from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.core.security import TokenPair
from app.db.models.enums import LanguageCode, UserRole
from app.services.auth_service import AuthService


def _mock_user() -> SimpleNamespace:
    return SimpleNamespace(
        id="11111111-1111-1111-1111-111111111111",
        email="auth@example.com",
        role=UserRole.USER,
        locale=LanguageCode.EN,
        timezone="UTC",
        is_active=True,
        is_verified=False,
        created_at=datetime.now(UTC),
    )


@pytest.mark.usefixtures("auth_overrides")
def test_register_login_refresh_logout_flow(client, monkeypatch):
    async def _register(self, payload):
        _ = payload
        return _mock_user(), TokenPair(
            access_token="access-1",
            refresh_token="refresh-1",
            token_type="bearer",
            expires_in=900,
        )

    async def _login(self, payload):
        _ = payload
        return _mock_user(), TokenPair(
            access_token="access-2",
            refresh_token="refresh-2",
            token_type="bearer",
            expires_in=900,
        )

    async def _refresh(self, refresh_token):
        _ = refresh_token
        return TokenPair(
            access_token="access-3",
            refresh_token="refresh-3",
            token_type="bearer",
            expires_in=900,
        )

    async def _logout(self, refresh_token):
        _ = refresh_token
        return None

    monkeypatch.setattr(AuthService, "register", _register)
    monkeypatch.setattr(AuthService, "login", _login)
    monkeypatch.setattr(AuthService, "refresh", _refresh)
    monkeypatch.setattr(AuthService, "logout", _logout)

    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "auth@example.com", "password": "password123", "locale": "en", "timezone": "UTC"},
    )
    assert register_response.status_code == 200
    assert register_response.json()["ok"] is True

    login_response = client.post("/api/v1/auth/login", json={"email": "auth@example.com", "password": "password123"})
    assert login_response.status_code == 200
    assert login_response.json()["data"]["tokens"]["refresh_token"] == "refresh-2"

    refresh_response = client.post("/api/v1/auth/refresh", json={"refresh_token": "refresh-2"})
    assert refresh_response.status_code == 200
    assert refresh_response.json()["data"]["access_token"] == "access-3"

    logout_response = client.post("/api/v1/auth/logout", json={"refresh_token": "refresh-3"})
    assert logout_response.status_code == 200
    assert logout_response.json()["data"]["logged_out"] is True


@pytest.mark.usefixtures("auth_overrides")
def test_refresh_replay_rejected(client, monkeypatch):
    async def _refresh(self, refresh_token):
        _ = refresh_token
        raise AppException(
            code=ErrorCode.AUTH_UNAUTHORIZED,
            message_key="errors.auth.refresh_revoked",
            status_code=401,
        )

    monkeypatch.setattr(AuthService, "refresh", _refresh)

    response = client.post("/api/v1/auth/refresh", json={"refresh_token": "already-used-refresh"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == ErrorCode.AUTH_UNAUTHORIZED.value
