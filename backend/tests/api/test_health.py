from fastapi.testclient import TestClient

from app.main import app


def test_healthcheck() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["data"]["status"] == "ok"
    assert response.headers["x-request-id"]


def test_healthcheck_propagates_request_id() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health", headers={"X-Request-ID": "req-health-123"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req-health-123"
