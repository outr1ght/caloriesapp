from datetime import timedelta

from app.core.security import create_token, parse_subject_from_token


def test_parse_subject_from_refresh_token() -> None:
    token = create_token(subject='user-1', token_type='refresh', expires_delta=timedelta(days=1))
    subject = parse_subject_from_token(token, expected_type='refresh')
    assert subject == 'user-1'


def test_parse_subject_from_wrong_type_token_returns_none() -> None:
    token = create_token(subject='user-1', token_type='access', expires_delta=timedelta(minutes=5))
    subject = parse_subject_from_token(token, expected_type='refresh')
    assert subject is None
