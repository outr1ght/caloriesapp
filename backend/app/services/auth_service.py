from datetime import UTC, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import AppException, ErrorCode
from app.core.security import TokenPair, create_token_pair, decode_token, hash_password, verify_password
from app.core.token_store import TokenStore
from app.db.models.enums import AuthProvider
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, OAuthLoginRequest, RegisterRequest

class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.token_store = TokenStore()

    async def register(self, payload: RegisterRequest) -> tuple[object, TokenPair]:
        existing = await self.users.get_by_email(payload.email)
        if existing is not None:
            raise AppException(code=ErrorCode.CONFLICT, message_key="errors.auth.email_already_used", status_code=409)
        user = await self.users.create_user(email=payload.email, hashed_password=hash_password(payload.password.get_secret_value()), locale=payload.locale.value, timezone=payload.timezone)
        await self.users.create_identity(user_id=user.id, provider=AuthProvider.LOCAL, provider_user_id=user.email, provider_email=user.email)
        await self.users.get_or_create_profile(user.id)
        tokens = create_token_pair(user.id)
        refresh_payload = decode_token(tokens.refresh_token)
        await self.token_store.allow_refresh_jti(refresh_payload.jti, ttl_days=30)
        await self.session.commit()
        return user, tokens

    async def login(self, payload: LoginRequest) -> tuple[object, TokenPair]:
        user = await self.users.get_by_email(payload.email)
        if user is None or not user.hashed_password or not verify_password(payload.password.get_secret_value(), user.hashed_password):
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.invalid_credentials", status_code=401)
        user.last_login_at = datetime.now(UTC)
        tokens = create_token_pair(user.id)
        refresh_payload = decode_token(tokens.refresh_token)
        await self.token_store.allow_refresh_jti(refresh_payload.jti, ttl_days=30)
        await self.session.commit()
        return user, tokens

    async def refresh(self, refresh_token: str) -> TokenPair:
        payload = decode_token(refresh_token)
        if payload.token_type.value != "refresh":
            raise AppException(code=ErrorCode.AUTH_INVALID_TOKEN, message_key="errors.auth.invalid_token_type", status_code=401)
        if not await self.token_store.is_refresh_allowed(payload.jti):
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.refresh_revoked", status_code=401)
        await self.token_store.revoke_refresh_jti(payload.jti, ttl_days=30)
        new_pair = create_token_pair(payload.sub)
        new_payload = decode_token(new_pair.refresh_token)
        await self.token_store.allow_refresh_jti(new_payload.jti, ttl_days=30)
        return new_pair

    async def logout(self, refresh_token: str | None) -> None:
        if not refresh_token:
            return
        try:
            payload = decode_token(refresh_token)
        except ValueError:
            return
        await self.token_store.revoke_refresh_jti(payload.jti, ttl_days=30)

    async def oauth_login(self, payload: OAuthLoginRequest) -> tuple[object, TokenPair]:
        if payload.provider == AuthProvider.LOCAL:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.invalid_oauth_provider", status_code=422)
        provider_user_id = payload.id_token or payload.code
        if not provider_user_id:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.oauth_missing_token", status_code=422)
        identity = await self.users.get_identity(payload.provider, provider_user_id)
        if identity is not None:
            user = identity.user
        else:
            synthetic_email = f"{payload.provider.value}_{provider_user_id[:16]}@oauth.local"
            user = await self.users.create_user(email=synthetic_email, hashed_password=None, locale="en", timezone="UTC")
            await self.users.create_identity(user_id=user.id, provider=payload.provider, provider_user_id=provider_user_id, provider_email=None)
            await self.users.get_or_create_profile(user.id)
        tokens = create_token_pair(user.id)
        rp = decode_token(tokens.refresh_token)
        await self.token_store.allow_refresh_jti(rp.jti, ttl_days=30)
        await self.session.commit()
        return user, tokens
