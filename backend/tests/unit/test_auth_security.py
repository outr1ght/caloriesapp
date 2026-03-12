from app.core.security import hash_password, verify_password


def test_password_hash_roundtrip() -> None:
    hashed = hash_password('Pass12345!')
    assert verify_password('Pass12345!', hashed)
