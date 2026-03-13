from datetime import UTC, datetime, timedelta

import pytest

from app.core.security import TokenType, _create_token, decode_token


def test_decode_refresh_token_payload() -> None:
    token = _create_token(subject="user-1", token_type=TokenType.REFRESH, expires_delta=timedelta(minutes=10))
    payload = decode_token(token)
    assert payload.sub == "user-1"
    assert payload.token_type == TokenType.REFRESH


def test_expired_token_rejected() -> None:
    token = _create_token(subject="user-1", token_type=TokenType.ACCESS, expires_delta=timedelta(seconds=-1))
    with pytest.raises(ValueError):
        decode_token(token)


def test_token_type_validation_path() -> None:
    token = _create_token(subject="user-1", token_type=TokenType.ACCESS, expires_delta=timedelta(minutes=10))
    payload = decode_token(token)
    assert payload.token_type == TokenType.ACCESS
    assert payload.exp > int(datetime.now(UTC).timestamp())
