from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi.security import HTTPAuthorizationCredentials

from app.common.exceptions import AppException, ErrorCode
from app.core.dependencies import get_current_user
from app.core.security import TokenType


class _Result:
    def __init__(self, user):
        self._user = user

    def scalar_one_or_none(self):
        return self._user


@pytest.mark.asyncio
async def test_get_current_user_requires_credentials() -> None:
    session = AsyncMock()

    with pytest.raises(AppException) as exc_info:
        await get_current_user(credentials=None, session=session)

    assert exc_info.value.code == ErrorCode.AUTH_UNAUTHORIZED
    assert exc_info.value.status_code == 401
    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_current_user_rejects_invalid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.core.dependencies.decode_token", lambda _: (_ for _ in ()).throw(ValueError("Invalid token")))
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid")
    session = AsyncMock()

    with pytest.raises(AppException) as exc_info:
        await get_current_user(credentials=credentials, session=session)

    assert exc_info.value.code == ErrorCode.AUTH_INVALID_TOKEN
    assert exc_info.value.status_code == 401
    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_current_user_rejects_wrong_token_type(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.core.dependencies.decode_token",
        lambda _: SimpleNamespace(sub="user-1", token_type=TokenType.REFRESH),
    )
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="refresh-token")
    session = AsyncMock()

    with pytest.raises(AppException) as exc_info:
        await get_current_user(credentials=credentials, session=session)

    assert exc_info.value.code == ErrorCode.AUTH_INVALID_TOKEN
    assert exc_info.value.message_key == "errors.auth.invalid_token_type"
    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_current_user_rejects_filtered_user(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.core.dependencies.decode_token",
        lambda _: SimpleNamespace(sub="user-1", token_type=TokenType.ACCESS),
    )
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="access-token")
    session = AsyncMock()
    session.execute.return_value = _Result(None)

    with pytest.raises(AppException) as exc_info:
        await get_current_user(credentials=credentials, session=session)

    assert exc_info.value.code == ErrorCode.AUTH_UNAUTHORIZED
    assert exc_info.value.message_key == "errors.auth.user_not_found"
    session.execute.assert_awaited_once()
