from types import SimpleNamespace

import pytest
from fastapi.security import HTTPAuthorizationCredentials

from app.common.exceptions import AppException
from app.core import dependencies
from app.core.security import TokenType


class _Result:
    def __init__(self, user):
        self._user = user

    def scalar_one_or_none(self):
        return self._user


class _Session:
    def __init__(self, user):
        self.user = user

    async def execute(self, stmt):
        _ = stmt
        return _Result(self.user)


@pytest.mark.asyncio
async def test_get_current_user_rejects_missing_credentials():
    with pytest.raises(AppException) as exc:
        await dependencies.get_current_user(credentials=None, session=_Session(user=None))
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_rejects_invalid_token(monkeypatch):
    def _decode(token):
        _ = token
        raise ValueError("invalid")

    monkeypatch.setattr(dependencies, "decode_token", _decode)

    with pytest.raises(AppException) as exc:
        await dependencies.get_current_user(
            credentials=HTTPAuthorizationCredentials(scheme="Bearer", credentials="bad"),
            session=_Session(user=None),
        )
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_rejects_deleted_or_inactive_user(monkeypatch):
    def _decode(token):
        _ = token
        return SimpleNamespace(sub="user-1", token_type=TokenType.ACCESS)

    monkeypatch.setattr(dependencies, "decode_token", _decode)

    with pytest.raises(AppException) as exc:
        await dependencies.get_current_user(
            credentials=HTTPAuthorizationCredentials(scheme="Bearer", credentials="ok"),
            session=_Session(user=None),
        )
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_returns_active_user(monkeypatch):
    user = SimpleNamespace(id="user-1", is_active=True, deleted_at=None)

    def _decode(token):
        _ = token
        return SimpleNamespace(sub="user-1", token_type=TokenType.ACCESS)

    monkeypatch.setattr(dependencies, "decode_token", _decode)

    current = await dependencies.get_current_user(
        credentials=HTTPAuthorizationCredentials(scheme="Bearer", credentials="ok"),
        session=_Session(user=user),
    )
    assert current.id == "user-1"
