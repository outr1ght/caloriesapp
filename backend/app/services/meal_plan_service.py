from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import AppException, ErrorCode
from app.db.models.meal import MealPlan
from app.schemas.meal_plans import MealPlanCreateRequest, MealPlanUpdateRequest

class MealPlanService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: str, payload: MealPlanCreateRequest) -> MealPlan:
        plan = MealPlan(user_id=user_id, plan_date=payload.plan_date, title=payload.title, notes=payload.notes, status=payload.status, meals_snapshot=[entry.model_dump() for entry in payload.entries])
        self.session.add(plan)
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def list(self, user_id: str) -> list[MealPlan]:
        result = await self.session.execute(select(MealPlan).where(MealPlan.user_id == user_id, MealPlan.deleted_at.is_(None)).order_by(MealPlan.plan_date.desc()))
        return list(result.scalars().all())

    async def update(self, user_id: str, plan_id: str, payload: MealPlanUpdateRequest) -> MealPlan:
        plan = await self.session.get(MealPlan, plan_id)
        if plan is None or plan.user_id != user_id or plan.deleted_at is not None:
            raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meal_plans.not_found", status_code=404)
        data = payload.model_dump(exclude_none=True)
        if "entries" in data:
            data["meals_snapshot"] = [entry.model_dump() for entry in payload.entries or []]
            del data["entries"]
        for k, v in data.items():
            setattr(plan, k, v)
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def delete(self, user_id: str, plan_id: str) -> None:
        plan = await self.session.get(MealPlan, plan_id)
        if plan is None or plan.user_id != user_id or plan.deleted_at is not None:
            raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meal_plans.not_found", status_code=404)
        plan.mark_deleted()
        await self.session.commit()
