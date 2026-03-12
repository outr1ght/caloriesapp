from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.core.database import get_session
from app.core.security import TokenType, decode_token
from app.db.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


async def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme), session: AsyncSession = Depends(db_session)) -> User:
    if credentials is None:
        raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.missing_credentials", status_code=401)

    payload = decode_token(credentials.credentials)
    if payload.token_type != TokenType.ACCESS:
        raise AppException(code=ErrorCode.AUTH_INVALID_TOKEN, message_key="errors.auth.invalid_token_type", status_code=401)

    result = await session.execute(select(User).where(User.id == payload.sub, User.is_active.is_(True), User.deleted_at.is_(None)))
    user = result.scalar_one_or_none()
    if user is None:
        raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.user_not_found", status_code=401)
    return user
