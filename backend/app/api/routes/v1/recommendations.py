from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.rate_limit import enforce_user_rate_limit
from app.db.models.domain_enums import RecommendationStatus, RecommendationType
from app.db.models.user import User
from app.schemas.recommendations import RecommendationUpdateStatusRequest
from app.services.recommendations_service import RecommendationsService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def _require_uuid(value: str) -> None:
    try:
        UUID(value)
    except ValueError as exc:
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.validation.invalid_uuid", status_code=422) from exc


@router.get("")
async def list_recommendations(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: RecommendationStatus | None = None,
    recommendation_type: RecommendationType | None = None,
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    rows, total = await RecommendationsService(session).list(current_user.id, page, page_size, status, recommendation_type)
    return success_response(
        data={
            "items": [
                {
                    "id": row.id,
                    "status": row.status.value,
                    "type": row.recommendation_type.value,
                    "title": row.title,
                }
                for row in rows
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@router.patch("/{recommendation_id}/status")
async def set_status(
    recommendation_id: str,
    payload: RecommendationUpdateStatusRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    _require_uuid(recommendation_id)
    updated = await RecommendationsService(session).set_status(current_user.id, recommendation_id, payload.status)
    return success_response(data={"id": updated.id, "status": updated.status.value})
