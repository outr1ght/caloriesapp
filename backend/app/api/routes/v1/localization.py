from fastapi import APIRouter, Depends

from app.common.responses import success_response
from app.core.dependencies import get_current_user
from app.core.serialization import serialize_api_data
from app.db.models.user import User
from app.schemas.localization import MessageLookupRequest
from app.services.localization_service import LocalizationService

router = APIRouter(prefix="/localization", tags=["localization"])


@router.get("/locales")
async def locales(_: User = Depends(get_current_user)) -> dict:
    return success_response(data=serialize_api_data([x.model_dump() for x in LocalizationService().get_supported_locales()]))


@router.post("/messages")
async def resolve_messages(payload: MessageLookupRequest, current_user: User = Depends(get_current_user)) -> dict:
    data = LocalizationService().resolve_messages(payload.keys, current_user.locale)
    return success_response(data=serialize_api_data({"locale": current_user.locale, "messages": data}))
