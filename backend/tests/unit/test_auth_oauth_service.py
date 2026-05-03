from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.db.models.enums import AuthProvider
from app.integrations.oauth.base import OAuthUserInfo
from app.services.auth_service import AuthService


class _Session:
    def __init__(self):
        self.commits = 0

    async def commit(self):
        self.commits += 1
        return None


@pytest.mark.asyncio
async def test_oauth_google_verified_token_creates_user_with_verified_provider_identity(monkeypatch):
    session = _Session()
    service = AuthService(session)
    oauth_user = OAuthUserInfo(provider_user_id="google-sub-123", email="user@gmail.com", email_verified=True, display_name="User")
    created_user = SimpleNamespace(id="user-1", email="user@gmail.com", is_active=True, deleted_at=None)
    identity_calls = []

    async def _resolve_user(**kwargs):
        _ = kwargs
        return oauth_user

    async def _get_identity(provider, provider_user_id):
        identity_calls.append((provider, provider_user_id))
        return None

    async def _create_user(**kwargs):
        assert kwargs["email"] == "user@gmail.com"
        return created_user

    async def _create_identity(**kwargs):
        identity_calls.append((kwargs["provider"], kwargs["provider_user_id"], kwargs["provider_email"]))
        return SimpleNamespace(**kwargs)

    async def _get_or_create_profile(user_id):
        _ = user_id
        return SimpleNamespace(user_id=user_id)

    async def _allow_refresh(jti):
        _ = jti
        return None

    monkeypatch.setattr(service, "_oauth_provider", lambda provider: SimpleNamespace(resolve_user=_resolve_user))
    monkeypatch.setattr(service.users, "get_identity", _get_identity)
    monkeypatch.setattr(service.users, "create_user", _create_user)
    monkeypatch.setattr(service.users, "create_identity", _create_identity)
    monkeypatch.setattr(service.users, "get_or_create_profile", _get_or_create_profile)
    monkeypatch.setattr(service, "_allow_refresh", _allow_refresh)
    monkeypatch.setattr("app.services.auth_service.create_token_pair", lambda _: SimpleNamespace(access_token="a", refresh_token="r", expires_in=900, token_type="bearer"))
    monkeypatch.setattr("app.services.auth_service.decode_token", lambda _: SimpleNamespace(jti="refresh-jti"))

    user, tokens = await service.oauth_login(SimpleNamespace(provider=AuthProvider.GOOGLE, id_token="raw-google-token", code=None, redirect_uri=None))

    assert user is created_user
    assert tokens.refresh_token == "r"
    assert identity_calls[0] == (AuthProvider.GOOGLE, "google-sub-123")
    assert identity_calls[1] == (AuthProvider.GOOGLE, "google-sub-123", "user@gmail.com")
    assert session.commits == 1


@pytest.mark.asyncio
async def test_oauth_apple_verified_token_logs_into_existing_identity(monkeypatch):
    session = _Session()
    service = AuthService(session)
    existing_user = SimpleNamespace(id="user-1", is_active=True, deleted_at=None)
    identity = SimpleNamespace(user=existing_user)
    oauth_user = OAuthUserInfo(provider_user_id="apple-sub-123", email="user@icloud.com", email_verified=True)

    async def _resolve_user(**kwargs):
        _ = kwargs
        return oauth_user

    async def _get_identity(provider, provider_user_id):
        assert provider == AuthProvider.APPLE
        assert provider_user_id == "apple-sub-123"
        return identity

    async def _allow_refresh(jti):
        _ = jti
        return None

    monkeypatch.setattr(service, "_oauth_provider", lambda provider: SimpleNamespace(resolve_user=_resolve_user))
    monkeypatch.setattr(service.users, "get_identity", _get_identity)
    monkeypatch.setattr(service, "_allow_refresh", _allow_refresh)
    monkeypatch.setattr("app.services.auth_service.create_token_pair", lambda _: SimpleNamespace(access_token="a", refresh_token="r", expires_in=900, token_type="bearer"))
    monkeypatch.setattr("app.services.auth_service.decode_token", lambda _: SimpleNamespace(jti="refresh-jti"))

    user, _ = await service.oauth_login(SimpleNamespace(provider=AuthProvider.APPLE, id_token="verified-apple-token", code=None, redirect_uri=None))

    assert user is existing_user
    assert session.commits == 1


@pytest.mark.asyncio
async def test_oauth_code_only_rejected():
    service = AuthService(_Session())

    with pytest.raises(AppException) as exc:
        await service.oauth_login(SimpleNamespace(provider=AuthProvider.GOOGLE, id_token=None, code="auth-code", redirect_uri="https://app/callback"))

    assert exc.value.code == ErrorCode.VALIDATION_ERROR
    assert exc.value.status_code == 422
    assert exc.value.message_key == "errors.auth.oauth_missing_token"


@pytest.mark.asyncio
async def test_raw_id_token_is_never_used_as_provider_user_id(monkeypatch):
    session = _Session()
    service = AuthService(session)
    raw_token = "raw-provider-token"
    seen = {}
    oauth_user = OAuthUserInfo(provider_user_id="verified-provider-sub", email=None, email_verified=False)
    created_user = SimpleNamespace(id="user-1", email="google_verified-pro@oauth.local", is_active=True, deleted_at=None)

    async def _resolve_user(**kwargs):
        _ = kwargs
        return oauth_user

    async def _get_identity(provider, provider_user_id):
        seen["lookup"] = provider_user_id
        return None

    async def _create_user(**kwargs):
        return created_user

    async def _create_identity(**kwargs):
        seen["created"] = kwargs["provider_user_id"]
        return SimpleNamespace(**kwargs)

    async def _get_or_create_profile(user_id):
        _ = user_id
        return SimpleNamespace(user_id=user_id)

    async def _allow_refresh(jti):
        _ = jti
        return None

    monkeypatch.setattr(service, "_oauth_provider", lambda provider: SimpleNamespace(resolve_user=_resolve_user))
    monkeypatch.setattr(service.users, "get_identity", _get_identity)
    monkeypatch.setattr(service.users, "create_user", _create_user)
    monkeypatch.setattr(service.users, "create_identity", _create_identity)
    monkeypatch.setattr(service.users, "get_or_create_profile", _get_or_create_profile)
    monkeypatch.setattr(service, "_allow_refresh", _allow_refresh)
    monkeypatch.setattr("app.services.auth_service.create_token_pair", lambda _: SimpleNamespace(access_token="a", refresh_token="r", expires_in=900, token_type="bearer"))
    monkeypatch.setattr("app.services.auth_service.decode_token", lambda _: SimpleNamespace(jti="refresh-jti"))

    await service.oauth_login(SimpleNamespace(provider=AuthProvider.GOOGLE, id_token=raw_token, code=None, redirect_uri=None))

    assert seen["lookup"] == "verified-provider-sub"
    assert seen["created"] == "verified-provider-sub"
    assert seen["lookup"] != raw_token
    assert seen["created"] != raw_token


@pytest.mark.asyncio
async def test_invalid_provider_token_rejected(monkeypatch):
    service = AuthService(_Session())

    async def _resolve_user(**kwargs):
        _ = kwargs
        raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)

    monkeypatch.setattr(service, "_oauth_provider", lambda provider: SimpleNamespace(resolve_user=_resolve_user))

    with pytest.raises(AppException) as exc:
        await service.oauth_login(SimpleNamespace(provider=AuthProvider.GOOGLE, id_token="bad-token", code=None, redirect_uri=None))

    assert exc.value.status_code == 401
    assert exc.value.message_key == "errors.auth.oauth_invalid_token"
