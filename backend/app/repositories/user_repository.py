from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.enums import AuthProvider
from app.db.models.user import AuthIdentity, User, UserProfile
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_id(self, user_id: str) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id, User.deleted_at.is_(None)))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email.lower().strip(), User.deleted_at.is_(None)))
        return result.scalar_one_or_none()

    async def create_user(self, *, email: str, hashed_password: str | None, locale: str, timezone: str) -> User:
        user = User(email=email.lower().strip(), hashed_password=hashed_password, locale=locale, timezone=timezone)  # type: ignore[arg-type]
        self.session.add(user)
        await self.session.flush()
        return user

    async def create_identity(self, *, user_id: str, provider: AuthProvider, provider_user_id: str, provider_email: str | None) -> AuthIdentity:
        identity = AuthIdentity(user_id=user_id, provider=provider, provider_user_id=provider_user_id, provider_email=provider_email)
        self.session.add(identity)
        await self.session.flush()
        return identity

    async def get_identity(self, provider: AuthProvider, provider_user_id: str) -> AuthIdentity | None:
        result = await self.session.execute(select(AuthIdentity).where(AuthIdentity.provider == provider, AuthIdentity.provider_user_id == provider_user_id))
        return result.scalar_one_or_none()

    async def get_or_create_profile(self, user_id: str) -> UserProfile:
        result = await self.session.execute(select(UserProfile).where(UserProfile.user_id == user_id, UserProfile.deleted_at.is_(None)))
        profile = result.scalar_one_or_none()
        if profile is not None:
            return profile
        profile = UserProfile(user_id=user_id)
        self.session.add(profile)
        await self.session.flush()
        return profile
