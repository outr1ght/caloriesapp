from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.schemas.profile import LocaleUpdateRequest, UserProfileUpdateRequest

class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def get_me(self, user_id: str):
        return await self.users.get_by_id(user_id)

    async def update_profile(self, user_id: str, payload: UserProfileUpdateRequest):
        profile = await self.users.get_or_create_profile(user_id)
        for key, value in payload.model_dump(exclude_none=True).items():
            setattr(profile, key, value)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def update_locale(self, user_id: str, payload: LocaleUpdateRequest):
        user = await self.users.get_by_id(user_id)
        if user is None:
            return None
        user.locale = payload.locale
        user.timezone = payload.timezone
        await self.session.commit()
        await self.session.refresh(user)
        return user
