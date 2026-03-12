from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.enums import LanguageCode
from app.db.models.progress import UserSettings
from app.db.models.user import User
from app.schemas.settings import UserSettingsUpdateRequest

class SettingsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_or_create(self, user: User) -> UserSettings:
        result = await self.session.execute(select(UserSettings).where(UserSettings.user_id == user.id))
        settings = result.scalar_one_or_none()
        if settings is not None:
            return settings
        settings = UserSettings(user_id=user.id, language=user.locale if isinstance(user.locale, LanguageCode) else LanguageCode.EN)
        self.session.add(settings)
        await self.session.commit()
        await self.session.refresh(settings)
        return settings

    async def update(self, user: User, payload: UserSettingsUpdateRequest) -> UserSettings:
        settings = await self.get_or_create(user)
        for key, value in payload.model_dump(exclude_none=True).items():
            setattr(settings, key, value)
        await self.session.commit()
        await self.session.refresh(settings)
        return settings
