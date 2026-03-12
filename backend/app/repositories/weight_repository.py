from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.progress import WeightLog
from app.repositories.base import BaseRepository


class WeightRepository(BaseRepository[WeightLog]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, entity: WeightLog) -> WeightLog:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get(self, user_id: str, log_id: str) -> WeightLog | None:
        result = await self.session.execute(select(WeightLog).where(WeightLog.user_id == user_id, WeightLog.id == log_id, WeightLog.deleted_at.is_(None)))
        return result.scalar_one_or_none()

    async def list(self, *, user_id: str, page: int, page_size: int, from_dt: datetime | None, to_dt: datetime | None) -> tuple[list[WeightLog], int]:
        filters = [WeightLog.user_id == user_id, WeightLog.deleted_at.is_(None)]
        if from_dt is not None:
            filters.append(WeightLog.logged_at >= from_dt)
        if to_dt is not None:
            filters.append(WeightLog.logged_at <= to_dt)
        rows = await self.session.execute(select(WeightLog).where(and_(*filters)).order_by(WeightLog.logged_at.desc()).offset((page - 1) * page_size).limit(page_size))
        count = await self.session.execute(select(func.count(WeightLog.id)).where(and_(*filters)))
        return list(rows.scalars().all()), int(count.scalar_one())
