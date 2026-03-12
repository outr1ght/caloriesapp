from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.domain_enums import RecommendationStatus, RecommendationType
from app.db.models.progress import Recommendation
from app.repositories.base import BaseRepository


class RecommendationRepository(BaseRepository[Recommendation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, entity: Recommendation) -> Recommendation:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def list_for_user(self, *, user_id: str, page: int, page_size: int, status: RecommendationStatus | None, recommendation_type: RecommendationType | None) -> tuple[list[Recommendation], int]:
        filters = [Recommendation.user_id == user_id, Recommendation.deleted_at.is_(None)]
        if status is not None:
            filters.append(Recommendation.status == status)
        if recommendation_type is not None:
            filters.append(Recommendation.recommendation_type == recommendation_type)
        rows = await self.session.execute(select(Recommendation).where(and_(*filters)).order_by(Recommendation.created_at.desc()).offset((page - 1) * page_size).limit(page_size))
        count = await self.session.execute(select(func.count(Recommendation.id)).where(and_(*filters)))
        return list(rows.scalars().all()), int(count.scalar_one())

    async def get(self, user_id: str, recommendation_id: str) -> Recommendation | None:
        result = await self.session.execute(select(Recommendation).where(Recommendation.id == recommendation_id, Recommendation.user_id == user_id, Recommendation.deleted_at.is_(None)))
        return result.scalar_one_or_none()
