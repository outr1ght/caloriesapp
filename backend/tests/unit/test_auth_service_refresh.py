import asyncio
from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.core.security import TokenPair
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

    async def _rotate(old_jti, new_jti):
        _ = (old_jti, new_jti)
        return False

    async def _get_by_id(user_id):
        _ = user_id
        return SimpleNamespace(id="user-1", is_active=True, deleted_at=None)

    monkeypatch.setattr("app.services.auth_service.decode_token", _decode_token)
    monkeypatch.setattr("app.services.auth_service.create_token_pair", lambda _: TokenPair(access_token="a", refresh_token="new-refresh", expires_in=900))
    monkeypatch.setattr(service, "_rotate_refresh_jti_atomically", _rotate)
    monkeypatch.setattr(service.users, "get_by_id", _get_by_id)

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

    async def _get_by_id(user_id):
        _ = user_id
        return inactive_user

    monkeypatch.setattr("app.services.auth_service.decode_token", _decode_token)
    monkeypatch.setattr(service.users, "get_by_id", _get_by_id)

    with pytest.raises(AppException) as exc:
        await service.refresh("refresh-token")

    assert exc.value.status_code == 401
    assert exc.value.message_key == "errors.auth.account_inactive"


@pytest.mark.asyncio
async def test_concurrent_refresh_allows_exactly_one_success(monkeypatch):
    service = AuthService(_Session())
    user = SimpleNamespace(id="user-1", is_active=True, deleted_at=None)
    decode_state = {"new_counter": 0}
    rotate_lock = asyncio.Lock()
    rotate_state = {"used": False}

    def _decode_token(token):
        if token == "old-refresh":
            return SimpleNamespace(sub="user-1", token_type=SimpleNamespace(value="refresh"), jti="old-jti")
        decode_state["new_counter"] += 1
        return SimpleNamespace(sub="user-1", token_type=SimpleNamespace(value="refresh"), jti=f"new-jti-{decode_state['new_counter']}")

    def _create_token_pair(_user_id):
        idx = decode_state["new_counter"] + 1
        return TokenPair(access_token=f"access-{idx}", refresh_token=f"refresh-{idx}", expires_in=900)

    async def _get_by_id(user_id):
        _ = user_id
        return user

    async def _rotate(old_jti, new_jti):
        _ = (old_jti, new_jti)
        async with rotate_lock:
            if rotate_state["used"]:
                return False
            rotate_state["used"] = True
            return True

    monkeypatch.setattr("app.services.auth_service.decode_token", _decode_token)
    monkeypatch.setattr("app.services.auth_service.create_token_pair", _create_token_pair)
    monkeypatch.setattr(service.users, "get_by_id", _get_by_id)
    monkeypatch.setattr(service, "_rotate_refresh_jti_atomically", _rotate)

    results = await asyncio.gather(
        service.refresh("old-refresh"),
        service.refresh("old-refresh"),
        return_exceptions=True,
    )

    successes = [result for result in results if not isinstance(result, Exception)]
    failures = [result for result in results if isinstance(result, Exception)]

    assert len(successes) == 1
    assert len(failures) == 1
    assert isinstance(failures[0], AppException)
    assert failures[0].status_code == 401
    assert failures[0].message_key == "errors.auth.refresh_revoked"


@pytest.mark.asyncio
async def test_refresh_redis_unavailable_returns_session_store_error(monkeypatch):
    service = AuthService(_Session())
    user = SimpleNamespace(id="user-1", is_active=True, deleted_at=None)

    def _decode_token(token):
        if token == "old-refresh":
            return SimpleNamespace(sub="user-1", token_type=SimpleNamespace(value="refresh"), jti="old-jti")
        return SimpleNamespace(sub="user-1", token_type=SimpleNamespace(value="refresh"), jti="new-jti")

    async def _get_by_id(user_id):
        _ = user_id
        return user

    async def _rotate(old_jti, new_jti):
        _ = (old_jti, new_jti)
        raise AppException(
            code=ErrorCode.INTERNAL_ERROR,
            message_key="errors.auth.session_store_unavailable",
            status_code=503,
        )

    monkeypatch.setattr("app.services.auth_service.decode_token", _decode_token)
    monkeypatch.setattr("app.services.auth_service.create_token_pair", lambda _: TokenPair(access_token="access", refresh_token="new-refresh", expires_in=900))
    monkeypatch.setattr(service.users, "get_by_id", _get_by_id)
    monkeypatch.setattr(service, "_rotate_refresh_jti_atomically", _rotate)

    with pytest.raises(AppException) as exc:
        await service.refresh("old-refresh")

    assert exc.value.status_code == 503
    assert exc.value.message_key == "errors.auth.session_store_unavailable"
