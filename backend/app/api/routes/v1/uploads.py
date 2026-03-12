from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.uploads import UploadCompleteRequest, UploadInitRequest
from app.services.upload_service import UploadService

router = APIRouter(prefix="/uploads", tags=["uploads"])

@router.post("/init")
async def init_upload(payload: UploadInitRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    return success_response(data=await UploadService(session).init_upload(current_user.id, payload))

@router.post("/complete")
async def complete_upload(payload: UploadCompleteRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    item = await UploadService(session).complete_upload(current_user.id, payload.upload_id)
    return success_response(data={"id": item.id, "storage_key": item.storage_key, "status": item.status.value})
