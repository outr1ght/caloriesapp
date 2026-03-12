from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import AppException, ErrorCode
from app.db.models.domain_enums import RecommendationStatus, RecommendationType
from app.db.models.progress import Recommendation
from app.repositories.recommendation_repository import RecommendationRepository

class RecommendationsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = RecommendationRepository(session)

    async def generate_daily_summary(self, user_id: str, body: str) -> Recommendation:
        entity = Recommendation(user_id=user_id, recommendation_type=RecommendationType.DAILY_SUMMARY, status=RecommendationStatus.READY, title="Daily nutrition summary", body=body, generator="hybrid")
        await self.repo.create(entity)
        await self.session.commit()
        return entity

    async def list(self, user_id: str, page: int, page_size: int, status, recommendation_type):
        return await self.repo.list_for_user(user_id=user_id, page=page, page_size=page_size, status=status, recommendation_type=recommendation_type)

    async def set_status(self, user_id: str, recommendation_id: str, status: RecommendationStatus) -> Recommendation:
        entity = await self.repo.get(user_id, recommendation_id)
        if entity is None:
            raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.recommendations.not_found", status_code=404)
        entity.status = status
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
