from datetime import timedelta

from app.core.security import TokenType, _create_token


def test_protected_route_requires_auth(client):
    response = client.get("/api/v1/me")
    assert response.status_code == 401
    assert response.json()["ok"] is False
    assert response.json()["message_key"] == "errors.auth.missing_credentials"


def test_wrong_token_type_rejected(client):
    token = _create_token(subject="user-1", token_type=TokenType.REFRESH, expires_delta=timedelta(minutes=10))
    response = client.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["message_key"] == "errors.auth.invalid_token_type"


def test_expired_access_token_rejected(client):
    token = _create_token(subject="user-1", token_type=TokenType.ACCESS, expires_delta=timedelta(seconds=-1))
    response = client.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["message_key"] == "errors.auth.invalid_token"


def test_malformed_access_token_rejected(client):
    response = client.get("/api/v1/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert response.status_code == 401
    body = response.json()
    assert body["ok"] is False
    assert body["message_key"] == "errors.auth.invalid_token"
    assert body["error"]["code"] == "AUTH_INVALID_TOKEN"
