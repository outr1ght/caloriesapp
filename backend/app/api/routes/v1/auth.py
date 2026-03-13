from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.responses import success_response
from app.core.database import get_session
from app.core.rate_limit import enforce_user_rate_limit
from app.schemas.auth import (
    AuthSessionResponse,
    AuthUserDTO,
    LoginRequest,
    LogoutRequest,
    OAuthLoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenPairDTO,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def _client_key(request: Request, scope: str) -> str:
    host = request.client.host if request.client else "unknown"
    return f"{scope}:{host}"


@router.post("/register")
async def register(payload: RegisterRequest, request: Request, session: AsyncSession = Depends(get_session)) -> dict:
    await enforce_user_rate_limit(request, _client_key(request, "auth_register"))
    service = AuthService(session)
    user, tokens = await service.register(payload)
    return success_response(
        data=AuthSessionResponse(
            user=AuthUserDTO.model_validate(user, from_attributes=True),
            tokens=TokenPairDTO(**tokens.model_dump()),
        ).model_dump()
    )


@router.post("/login")
async def login(payload: LoginRequest, request: Request, session: AsyncSession = Depends(get_session)) -> dict:
    await enforce_user_rate_limit(request, _client_key(request, "auth_login"))
    service = AuthService(session)
    user, tokens = await service.login(payload)
    return success_response(
        data=AuthSessionResponse(
            user=AuthUserDTO.model_validate(user, from_attributes=True),
            tokens=TokenPairDTO(**tokens.model_dump()),
        ).model_dump()
    )


@router.post("/refresh")
async def refresh(payload: RefreshTokenRequest, request: Request, session: AsyncSession = Depends(get_session)) -> dict:
    await enforce_user_rate_limit(request, _client_key(request, "auth_refresh"))
    service = AuthService(session)
    tokens = await service.refresh(payload.refresh_token)
    return success_response(data=TokenPairDTO(**tokens.model_dump()).model_dump())


@router.post("/logout")
async def logout(payload: LogoutRequest, request: Request, session: AsyncSession = Depends(get_session)) -> dict:
    await enforce_user_rate_limit(request, _client_key(request, "auth_logout"))
    service = AuthService(session)
    await service.logout(payload.refresh_token)
    return success_response(data={"logged_out": True})


@router.post("/oauth")
async def oauth_login(payload: OAuthLoginRequest, request: Request, session: AsyncSession = Depends(get_session)) -> dict:
    await enforce_user_rate_limit(request, _client_key(request, "auth_oauth"))
    service = AuthService(session)
    user, tokens = await service.oauth_login(payload)
    return success_response(
        data=AuthSessionResponse(
            user=AuthUserDTO.model_validate(user, from_attributes=True),
            tokens=TokenPairDTO(**tokens.model_dump()),
        ).model_dump()
    )
