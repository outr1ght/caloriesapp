from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.services.auth_service import AuthService


class _Session:
    async def commit(self):
        return None


@pytest.mark.asyncio
async def test_refresh_rejects_replay(monkeypatch):
    service = AuthService(_Session())

    def _decode_token(token):
        _ = token
        return SimpleNamespace(sub="user-1", token_type=SimpleNamespace(value="refresh"), jti="jti-1")

    async def _is_allowed(jti):
        _ = jti
        return False

    monkeypatch.setattr("app.services.auth_service.decode_token", _decode_token)
    monkeypatch.setattr(service, "_is_refresh_allowed", _is_allowed)

    with pytest.raises(AppException) as exc:
        await service.refresh("used-token")
    assert exc.value.status_code == 401
    assert exc.value.message_key == "errors.auth.refresh_revoked"


@pytest.mark.asyncio
async def test_login_rejects_inactive_user(monkeypatch):
    service = AuthService(_Session())
    inactive_user = SimpleNamespace(
        id="user-1",
        email="inactive@example.com",
        hashed_password="hashed",
        is_active=False,
        deleted_at=None,
    )

    async def _get_by_email(email):
        _ = email
        return inactive_user

    monkeypatch.setattr(service.users, "get_by_email", _get_by_email)
    monkeypatch.setattr("app.services.auth_service.verify_password", lambda plain, hashed: True)

    with pytest.raises(AppException) as exc:
        await service.login(SimpleNamespace(email="inactive@example.com", password=SimpleNamespace(get_secret_value=lambda: "password123")))

    assert exc.value.status_code == 401
    assert exc.value.message_key == "errors.auth.account_inactive"


@pytest.mark.asyncio
async def test_refresh_rejects_inactive_user(monkeypatch):
    service = AuthService(_Session())
    inactive_user = SimpleNamespace(id="user-1", is_active=False, deleted_at=None)

    def _decode_token(token):
        _ = token
        return SimpleNamespace(sub="user-1", token_type=SimpleNamespace(value="refresh"), jti="jti-1")

    async def _is_allowed(jti):
        _ = jti
        return True

    async def _get_by_id(user_id):
        _ = user_id
        return inactive_user

    monkeypatch.setattr("app.services.auth_service.decode_token", _decode_token)
    monkeypatch.setattr(service, "_is_refresh_allowed", _is_allowed)
    monkeypatch.setattr(service.users, "get_by_id", _get_by_id)

    with pytest.raises(AppException) as exc:
        await service.refresh("refresh-token")

    assert exc.value.status_code == 401
    assert exc.value.message_key == "errors.auth.account_inactive"
