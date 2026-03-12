from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.meal_plans import MealPlanCreateRequest, MealPlanUpdateRequest
from app.services.meal_plan_service import MealPlanService

router = APIRouter(prefix="/meal-plans", tags=["meal-plans"])

@router.post("")
async def create_plan(payload: MealPlanCreateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    plan = await MealPlanService(session).create(current_user.id, payload)
    return success_response(data={"id": plan.id, "status": plan.status.value, "plan_date": plan.plan_date.isoformat()})

@router.get("")
async def list_plans(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    rows = await MealPlanService(session).list(current_user.id)
    return success_response(data={"items": [{"id": r.id, "status": r.status.value, "plan_date": r.plan_date.isoformat(), "title": r.title} for r in rows]})

@router.patch("/{plan_id}")
async def update_plan(plan_id: str, payload: MealPlanUpdateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    row = await MealPlanService(session).update(current_user.id, plan_id, payload)
    return success_response(data={"id": row.id, "status": row.status.value})

@router.delete("/{plan_id}")
async def delete_plan(plan_id: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    await MealPlanService(session).delete(current_user.id, plan_id)
    return success_response(data={"deleted": True})
