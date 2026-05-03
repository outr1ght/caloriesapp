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
from app.db.models.user import User
from app.schemas.weight_logs import WeightLogCreateRequest, WeightLogListQuery, WeightLogUpdateRequest
from app.services.weight_log_service import WeightLogService

router = APIRouter(prefix="/weights", tags=["weights"])


class WeightLogListItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    logged_at: str
    weight_kg: str


class WeightLogListDataResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[WeightLogListItemResponse]
    meta: PaginationMeta


class WeightLogListEnvelopeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    message_key: str
    data: WeightLogListDataResponse
    error: None = None
    meta: dict[str, Any] = Field(default_factory=dict)


def _require_uuid(value: str) -> None:
    try:
        UUID(value)
    except ValueError as exc:
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.validation.invalid_uuid", status_code=422) from exc


@router.post("")
async def create_weight(
    payload: WeightLogCreateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    row = await WeightLogService(session).create(current_user.id, payload)
    return success_response(data=serialize_api_data({"id": row.id, "logged_at": row.logged_at, "weight_kg": row.weight_kg}))


@router.get("", response_model=WeightLogListEnvelopeResponse)
async def list_weights(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=30, ge=1, le=200),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    rows, total = await WeightLogService(session).list(current_user.id, WeightLogListQuery(page=page, page_size=page_size))
    return success_response(
        data=serialize_api_data(
            build_paginated_data(
                items=[{"id": item.id, "logged_at": item.logged_at, "weight_kg": item.weight_kg} for item in rows],
                page=page,
                page_size=page_size,
                total=total,
            )
        )
    )


@router.patch("/{log_id}")
async def update_weight(
    log_id: str,
    payload: WeightLogUpdateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    _require_uuid(log_id)
    row = await WeightLogService(session).update(current_user.id, log_id, payload)
    return success_response(data=serialize_api_data({"id": row.id, "weight_kg": row.weight_kg}))


@router.delete("/{log_id}")
async def delete_weight(
    log_id: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    _require_uuid(log_id)
    await WeightLogService(session).delete(current_user.id, log_id)
    return success_response(data={"deleted": True})
