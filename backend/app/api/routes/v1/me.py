from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.profile import LocaleUpdateRequest, MeDTO, UserProfileDTO, UserProfileUpdateRequest
from app.services.user_service import UserService

router = APIRouter(prefix="/me", tags=["me"])

@router.get("")
async def me(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    service = UserService(session)
    user = await service.get_me(current_user.id)
    profile = user.profile if user else None
    dto = MeDTO(id=current_user.id, email=current_user.email, role=current_user.role, locale=current_user.locale, timezone=current_user.timezone, is_active=current_user.is_active, is_verified=current_user.is_verified, created_at=current_user.created_at, profile=UserProfileDTO.model_validate(profile, from_attributes=True) if profile else None)
    return success_response(data=dto.model_dump())

@router.patch("/profile")
async def update_profile(payload: UserProfileUpdateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    service = UserService(session)
    profile = await service.update_profile(current_user.id, payload)
    return success_response(data=UserProfileDTO.model_validate(profile, from_attributes=True).model_dump())

@router.patch("/locale")
async def update_locale(payload: LocaleUpdateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    service = UserService(session)
    user = await service.update_locale(current_user.id, payload)
    return success_response(data={"locale": user.locale.value if user else current_user.locale.value, "timezone": user.timezone if user else current_user.timezone})
