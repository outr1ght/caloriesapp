from datetime import UTC, datetime, timedelta
from enum import StrEnum
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field, ValidationError

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload(BaseModel):
    sub: str = Field(description="User ID")
    token_type: TokenType
    exp: int
    iat: int
    jti: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def _create_token(subject: str, token_type: TokenType, expires_delta: timedelta) -> str:
    now = datetime.now(UTC)
    expire = now + expires_delta
    payload = {"sub": subject, "token_type": token_type.value, "iat": int(now.timestamp()), "exp": int(expire.timestamp()), "jti": str(uuid4())}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str) -> str:
    return _create_token(subject=subject, token_type=TokenType.ACCESS, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))


def create_refresh_token(subject: str) -> str:
    return _create_token(subject=subject, token_type=TokenType.REFRESH, expires_delta=timedelta(days=settings.refresh_token_expire_days))


def decode_token(token: str) -> TokenPayload:
    try:
        raw_payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        return TokenPayload.model_validate(raw_payload)
    except (JWTError, ValidationError) as exc:
        raise ValueError("Invalid token") from exc


def create_token_pair(user_id: str) -> TokenPair:
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    return TokenPair(access_token=access, refresh_token=refresh, expires_in=settings.access_token_expire_minutes * 60)
