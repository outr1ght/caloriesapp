from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.meal import Meal, MealItem
from app.repositories.base import BaseRepository


class MealRepository(BaseRepository[Meal]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_meal(self, meal: Meal) -> Meal:
        self.session.add(meal)
        await self.session.flush()
        return meal

    async def get_meal(self, user_id: str, meal_id: str) -> Meal | None:
        result = await self.session.execute(select(Meal).where(Meal.id == meal_id, Meal.user_id == user_id, Meal.deleted_at.is_(None)).options(selectinload(Meal.items)))
        return result.scalar_one_or_none()

    async def list_meals(self, *, user_id: str, page: int, page_size: int, from_dt: datetime | None, to_dt: datetime | None) -> tuple[list[Meal], int]:
        filters = [Meal.user_id == user_id, Meal.deleted_at.is_(None)]
        if from_dt is not None:
            filters.append(Meal.eaten_at >= from_dt)
        if to_dt is not None:
            filters.append(Meal.eaten_at <= to_dt)

        result = await self.session.execute(select(Meal).where(and_(*filters)).order_by(Meal.eaten_at.desc()).offset((page - 1) * page_size).limit(page_size).options(selectinload(Meal.items)))
        count_result = await self.session.execute(select(func.count(Meal.id)).where(and_(*filters)))
        return list(result.scalars().all()), int(count_result.scalar_one())

    async def add_item(self, item: MealItem) -> MealItem:
        self.session.add(item)
        await self.session.flush()
        return item
