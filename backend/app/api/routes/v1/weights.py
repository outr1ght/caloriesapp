from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.weight_logs import WeightLogCreateRequest, WeightLogListQuery, WeightLogUpdateRequest
from app.services.weight_log_service import WeightLogService

router = APIRouter(prefix="/weights", tags=["weights"])

@router.post("")
async def create_weight(payload: WeightLogCreateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    row = await WeightLogService(session).create(current_user.id, payload)
    return success_response(data={"id": row.id, "logged_at": row.logged_at.isoformat(), "weight_kg": str(row.weight_kg)})

@router.get("")
async def list_weights(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session), page: int = Query(default=1, ge=1), page_size: int = Query(default=30, ge=1, le=200)) -> dict:
    rows, total = await WeightLogService(session).list(current_user.id, WeightLogListQuery(page=page, page_size=page_size))
    return success_response(data={"items": [{"id": x.id, "logged_at": x.logged_at.isoformat(), "weight_kg": str(x.weight_kg)} for x in rows], "total": total, "page": page, "page_size": page_size})

@router.patch("/{log_id}")
async def update_weight(log_id: str, payload: WeightLogUpdateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    row = await WeightLogService(session).update(current_user.id, log_id, payload)
    return success_response(data={"id": row.id, "weight_kg": str(row.weight_kg)})

@router.delete("/{log_id}")
async def delete_weight(log_id: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    await WeightLogService(session).delete(current_user.id, log_id)
    return success_response(data={"deleted": True})
