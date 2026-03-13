from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.rate_limit import enforce_user_rate_limit
from app.db.models.user import User
from app.schemas.uploads import UploadCompleteRequest, UploadInitRequest
from app.services.upload_service import UploadService

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/init")
async def init_upload(
    payload: UploadInitRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    return success_response(data=await UploadService(session).init_upload(current_user.id, payload))


@router.post("/complete")
async def complete_upload(
    payload: UploadCompleteRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    try:
        UUID(payload.upload_id)
    except ValueError as exc:
        raise AppException(
            code=ErrorCode.VALIDATION_ERROR,
            message_key="errors.validation.invalid_uuid",
            status_code=422,
        ) from exc

    item = await UploadService(session).complete_upload(current_user.id, payload.upload_id)
    return success_response(data={"id": item.id, "storage_key": item.storage_key, "status": item.status.value})
