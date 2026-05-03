from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import jwt
import pytest

from app.common.exceptions import AppException
from app.integrations.oauth.apple import AppleOAuthProvider
from app.integrations.oauth.google import GoogleOAuthProvider


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


class _FakeAsyncClient:
    def __init__(self, response: _FakeResponse):
        self.response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        _ = (exc_type, exc, tb)
        return False

    async def get(self, url, params):
        _ = (url, params)
        return self.response


class _FakeSigningKey:
    def __init__(self, key: str):
        self.key = key


class _FakeJWKClient:
    def __init__(self, jwks_url: str):
        self.jwks_url = jwks_url

    def get_signing_key_from_jwt(self, token: str):
        _ = token
        return _FakeSigningKey("public-key")


@pytest.mark.asyncio
async def test_google_provider_accepts_verified_token(monkeypatch):
    future_exp = int((datetime.now(UTC) + timedelta(minutes=10)).timestamp())
    response = _FakeResponse(
        200,
        {
            "sub": "google-sub-1",
            "email": "user@gmail.com",
            "email_verified": "true",
            "name": "User",
            "aud": "google-client-id",
            "iss": "https://accounts.google.com",
            "exp": str(future_exp),
        },
    )
    monkeypatch.setattr("app.integrations.oauth.google.get_settings", lambda: SimpleNamespace(google_oauth_client_id="google-client-id"))
    monkeypatch.setattr("app.integrations.oauth.google.httpx.AsyncClient", lambda timeout=10: _FakeAsyncClient(response))

    result = await GoogleOAuthProvider().resolve_user(code=None, id_token="verified-token", redirect_uri=None)

    assert result.provider_user_id == "google-sub-1"
    assert result.email == "user@gmail.com"
    assert result.email_verified is True


@pytest.mark.asyncio
async def test_google_provider_rejects_invalid_token(monkeypatch):
    future_exp = int((datetime.now(UTC) + timedelta(minutes=10)).timestamp())
    response = _FakeResponse(
        200,
        {
            "sub": "google-sub-1",
            "email": "user@gmail.com",
            "email_verified": "true",
            "aud": "wrong-client-id",
            "iss": "https://accounts.google.com",
            "exp": str(future_exp),
        },
    )
    monkeypatch.setattr("app.integrations.oauth.google.get_settings", lambda: SimpleNamespace(google_oauth_client_id="google-client-id"))
    monkeypatch.setattr("app.integrations.oauth.google.httpx.AsyncClient", lambda timeout=10: _FakeAsyncClient(response))

    with pytest.raises(AppException) as exc:
        await GoogleOAuthProvider().resolve_user(code=None, id_token="bad-token", redirect_uri=None)

    assert exc.value.status_code == 401
    assert exc.value.message_key == "errors.auth.oauth_invalid_token"


@pytest.mark.asyncio
async def test_apple_provider_accepts_verified_token(monkeypatch):
    monkeypatch.setattr("app.integrations.oauth.apple.get_settings", lambda: SimpleNamespace(apple_oauth_client_id="apple-client-id", apple_oauth_jwks_url="https://appleid.apple.com/auth/keys"))
    monkeypatch.setattr("app.integrations.oauth.apple.PyJWKClient", _FakeJWKClient)
    monkeypatch.setattr(
        "app.integrations.oauth.apple.jwt.decode",
        lambda token, key, algorithms, audience, issuer: {
            "sub": "apple-sub-1",
            "email": "user@icloud.com",
            "email_verified": "true",
        },
    )

    result = await AppleOAuthProvider().resolve_user(code=None, id_token="verified-token", redirect_uri=None)

    assert result.provider_user_id == "apple-sub-1"
    assert result.email == "user@icloud.com"
    assert result.email_verified is True


@pytest.mark.asyncio
async def test_apple_provider_rejects_invalid_token(monkeypatch):
    monkeypatch.setattr("app.integrations.oauth.apple.get_settings", lambda: SimpleNamespace(apple_oauth_client_id="apple-client-id", apple_oauth_jwks_url="https://appleid.apple.com/auth/keys"))
    monkeypatch.setattr("app.integrations.oauth.apple.PyJWKClient", _FakeJWKClient)

    def _decode(*args, **kwargs):
        _ = (args, kwargs)
        raise jwt.InvalidTokenError("invalid")

    monkeypatch.setattr("app.integrations.oauth.apple.jwt.decode", _decode)

    with pytest.raises(AppException) as exc:
        await AppleOAuthProvider().resolve_user(code=None, id_token="bad-token", redirect_uri=None)

    assert exc.value.status_code == 401
    assert exc.value.message_key == "errors.auth.oauth_invalid_token"
