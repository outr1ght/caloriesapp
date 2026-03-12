from app.schemas.auth import LoginRequest, RegisterRequest

def test_register_payload_validation() -> None:
    payload = RegisterRequest(email="user@example.com", password="password123", locale="en", timezone="UTC")
    assert payload.email == "user@example.com"

def test_login_payload_validation() -> None:
    payload = LoginRequest(email="user@example.com", password="password123")
    assert payload.email == "user@example.com"
