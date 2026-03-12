from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import success_response
from app.core.database import get_session
from app.schemas.auth import AuthSessionResponse, AuthUserDTO, LoginRequest, LogoutRequest, OAuthLoginRequest, RefreshTokenRequest, RegisterRequest, TokenPairDTO
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_session)) -> dict:
    service = AuthService(session)
    user, tokens = await service.register(payload)
    return success_response(data=AuthSessionResponse(user=AuthUserDTO.model_validate(user, from_attributes=True), tokens=TokenPairDTO(**tokens.model_dump())).model_dump())

@router.post("/login")
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)) -> dict:
    service = AuthService(session)
    user, tokens = await service.login(payload)
    return success_response(data=AuthSessionResponse(user=AuthUserDTO.model_validate(user, from_attributes=True), tokens=TokenPairDTO(**tokens.model_dump())).model_dump())

@router.post("/refresh")
async def refresh(payload: RefreshTokenRequest, session: AsyncSession = Depends(get_session)) -> dict:
    service = AuthService(session)
    tokens = await service.refresh(payload.refresh_token)
    return success_response(data=TokenPairDTO(**tokens.model_dump()).model_dump())

@router.post("/logout")
async def logout(payload: LogoutRequest, session: AsyncSession = Depends(get_session)) -> dict:
    service = AuthService(session)
    await service.logout(payload.refresh_token)
    return success_response(data={"logged_out": True})

@router.post("/oauth")
async def oauth_login(payload: OAuthLoginRequest, session: AsyncSession = Depends(get_session)) -> dict:
    service = AuthService(session)
    user, tokens = await service.oauth_login(payload)
    return success_response(data=AuthSessionResponse(user=AuthUserDTO.model_validate(user, from_attributes=True), tokens=TokenPairDTO(**tokens.model_dump())).model_dump())
