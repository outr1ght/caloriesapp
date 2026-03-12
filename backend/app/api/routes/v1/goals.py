from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.goals import NutritionGoalCreateRequest, NutritionGoalDTO, NutritionGoalUpdateRequest
from app.services.goals_service import GoalsService

router = APIRouter(prefix="/goals", tags=["goals"])

@router.get("/active")
async def get_active_goal(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    service = GoalsService(session)
    goal = await service.get_active_goal(current_user.id)
    return success_response(data=NutritionGoalDTO.model_validate(goal, from_attributes=True).model_dump() if goal else None)

@router.post("")
async def create_goal(payload: NutritionGoalCreateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    service = GoalsService(session)
    goal = await service.create_goal(current_user.id, payload)
    return success_response(data=NutritionGoalDTO.model_validate(goal, from_attributes=True).model_dump())

@router.patch("/{goal_id}")
async def update_goal(goal_id: str, payload: NutritionGoalUpdateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> dict:
    service = GoalsService(session)
    goal = await service.update_goal(current_user.id, goal_id, payload)
    return success_response(data=NutritionGoalDTO.model_validate(goal, from_attributes=True).model_dump())
