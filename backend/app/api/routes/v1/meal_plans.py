from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.rate_limit import enforce_user_rate_limit
from app.db.models.user import User
from app.schemas.meal_plans import MealPlanCreateRequest, MealPlanUpdateRequest
from app.services.meal_plan_service import MealPlanService

router = APIRouter(prefix="/meal-plans", tags=["meal-plans"])


def _require_uuid(value: str) -> None:
    try:
        UUID(value)
    except ValueError as exc:
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.validation.invalid_uuid", status_code=422) from exc


@router.post("")
async def create_plan(
    payload: MealPlanCreateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    plan = await MealPlanService(session).create(current_user.id, payload)
    return success_response(data={"id": plan.id, "status": plan.status.value, "plan_date": plan.plan_date.isoformat()})


@router.get("")
async def list_plans(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    rows = await MealPlanService(session).list(current_user.id)
    return success_response(
        data={
            "items": [
                {"id": row.id, "status": row.status.value, "plan_date": row.plan_date.isoformat(), "title": row.title}
                for row in rows
            ]
        }
    )


@router.patch("/{plan_id}")
async def update_plan(
    plan_id: str,
    payload: MealPlanUpdateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    _require_uuid(plan_id)
    row = await MealPlanService(session).update(current_user.id, plan_id, payload)
    return success_response(data={"id": row.id, "status": row.status.value})


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    _require_uuid(plan_id)
    await MealPlanService(session).delete(current_user.id, plan_id)
    return success_response(data={"deleted": True})
