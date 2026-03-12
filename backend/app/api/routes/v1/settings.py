from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.settings import UserSettingsDTO, UserSettingsUpdateRequest
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("")
async def get_settings(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    service = SettingsService(session)
    settings = await service.get_or_create(current_user)
    return success_response(data=UserSettingsDTO.model_validate(settings, from_attributes=True).model_dump())

@router.patch("")
async def update_settings(payload: UserSettingsUpdateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    service = SettingsService(session)
    settings = await service.update(current_user, payload)
    return success_response(data=UserSettingsDTO.model_validate(settings, from_attributes=True).model_dump())
