from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.db.models.domain_enums import RecommendationStatus, RecommendationType
from app.db.models.user import User
from app.schemas.recommendations import RecommendationUpdateStatusRequest
from app.services.recommendations_service import RecommendationsService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("")
async def list_recommendations(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session), page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=100), status: RecommendationStatus | None = None, recommendation_type: RecommendationType | None = None) -> dict:
    rows, total = await RecommendationsService(session).list(current_user.id, page, page_size, status, recommendation_type)
    return success_response(data={"items": [{"id": r.id, "status": r.status.value, "type": r.recommendation_type.value, "title": r.title} for r in rows], "total": total, "page": page, "page_size": page_size})

@router.patch("/{recommendation_id}/status")
async def set_status(recommendation_id: str, payload: RecommendationUpdateStatusRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    updated = await RecommendationsService(session).set_status(current_user.id, recommendation_id, payload.status)
    return success_response(data={"id": updated.id, "status": updated.status.value})
