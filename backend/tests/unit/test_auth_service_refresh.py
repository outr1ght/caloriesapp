from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException
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
