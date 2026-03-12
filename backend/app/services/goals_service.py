from datetime import UTC, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import AppException, ErrorCode
from app.db.models.progress import NutritionGoal
from app.schemas.goals import NutritionGoalCreateRequest, NutritionGoalUpdateRequest

class GoalsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_goal(self, user_id: str) -> NutritionGoal | None:
        result = await self.session.execute(select(NutritionGoal).where(NutritionGoal.user_id == user_id, NutritionGoal.is_active.is_(True), NutritionGoal.deleted_at.is_(None)))
        return result.scalar_one_or_none()

    async def create_goal(self, user_id: str, payload: NutritionGoalCreateRequest) -> NutritionGoal:
        current = await self.get_active_goal(user_id)
        if current is not None:
            current.is_active = False
            current.effective_to = datetime.now(UTC)
        goal = NutritionGoal(user_id=user_id, strategy=payload.strategy, activity_level=payload.activity_level, target_calories=payload.target_calories, target_protein_g=payload.target_protein_g, target_carbs_g=payload.target_carbs_g, target_fat_g=payload.target_fat_g, target_water_ml=payload.target_water_ml, is_active=True, effective_from=payload.effective_from, effective_to=None)
        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def update_goal(self, user_id: str, goal_id: str, payload: NutritionGoalUpdateRequest) -> NutritionGoal:
        goal = await self.session.get(NutritionGoal, goal_id)
        if goal is None or goal.user_id != user_id or goal.deleted_at is not None:
            raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.goals.not_found", status_code=404)
        for key, value in payload.model_dump(exclude_none=True).items():
            setattr(goal, key, value)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal
