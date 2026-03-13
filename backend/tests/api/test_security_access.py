from datetime import timedelta

from app.core.security import TokenType, _create_token


def test_protected_route_requires_auth(client):
    response = client.get("/api/v1/me")
    assert response.status_code == 401


def test_wrong_token_type_rejected(client):
    token = _create_token(subject="user-1", token_type=TokenType.REFRESH, expires_delta=timedelta(minutes=10))
    response = client.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_expired_access_token_rejected(client):
    token = _create_token(subject="user-1", token_type=TokenType.ACCESS, expires_delta=timedelta(seconds=-1))
    response = client.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
