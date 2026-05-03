from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.pagination import PaginationMeta, build_paginated_data
from app.core.rate_limit import enforce_user_rate_limit
from app.core.serialization import serialize_api_data
from app.db.models.domain_enums import RecommendationStatus, RecommendationType
from app.db.models.user import User
from app.schemas.recommendations import RecommendationUpdateStatusRequest
from app.services.recommendations_service import RecommendationsService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class RecommendationListItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    status: str
    type: str
    title: str


class RecommendationListDataResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[RecommendationListItemResponse]
    meta: PaginationMeta


class RecommendationListEnvelopeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    message_key: str
    data: RecommendationListDataResponse
    error: None = None
    meta: dict[str, Any] = Field(default_factory=dict)


def _require_uuid(value: str) -> None:
    try:
        UUID(value)
    except ValueError as exc:
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.validation.invalid_uuid", status_code=422) from exc


@router.get("", response_model=RecommendationListEnvelopeResponse)
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
        data=serialize_api_data(
            build_paginated_data(
                items=[
                    {
                        "id": row.id,
                        "status": row.status,
                        "type": row.recommendation_type,
                        "title": row.title,
                    }
                    for row in rows
                ],
                page=page,
                page_size=page_size,
                total=total,
            )
        )
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
    return success_response(data=serialize_api_data({"id": updated.id, "status": updated.status}))
