from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import AppException, ErrorCode
from app.db.models.progress import WeightLog
from app.repositories.weight_repository import WeightRepository
from app.schemas.weight_logs import WeightLogCreateRequest, WeightLogListQuery, WeightLogUpdateRequest

class WeightLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = WeightRepository(session)

    async def create(self, user_id: str, payload: WeightLogCreateRequest) -> WeightLog:
        entity = WeightLog(user_id=user_id, logged_at=payload.logged_at, weight_kg=payload.weight_kg, body_fat_percent=payload.body_fat_percent, note=payload.note)
        await self.repo.create(entity)
        await self.session.commit()
        return entity

    async def list(self, user_id: str, query: WeightLogListQuery):
        return await self.repo.list(user_id=user_id, page=query.page, page_size=query.page_size, from_dt=query.from_dt, to_dt=query.to_dt)

    async def update(self, user_id: str, log_id: str, payload: WeightLogUpdateRequest) -> WeightLog:
        entity = await self.repo.get(user_id, log_id)
        if entity is None:
            raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.weights.not_found", status_code=404)
        for k, v in payload.model_dump(exclude_none=True).items():
            setattr(entity, k, v)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, user_id: str, log_id: str) -> None:
        entity = await self.repo.get(user_id, log_id)
        if entity is None:
            raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.weights.not_found", status_code=404)
        entity.mark_deleted()
        await self.session.commit()
