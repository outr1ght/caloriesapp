from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.core.config import get_settings
from app.core.security import TokenPair, create_token_pair, decode_token, hash_password, verify_password
from app.core.token_store import TokenStore
from app.db.models.enums import AuthProvider
from app.integrations.oauth.apple import AppleOAuthProvider
from app.integrations.oauth.base import OAuthProvider
from app.integrations.oauth.google import GoogleOAuthProvider
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, OAuthLoginRequest, RegisterRequest


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.token_store = TokenStore()
        self.settings = get_settings()

    def _refresh_ttl_days(self) -> int:
        return self.settings.refresh_token_expire_days

    @staticmethod
    def _ensure_active_user(user: object | None) -> object:
        if user is None or getattr(user, "deleted_at", None) is not None or not bool(getattr(user, "is_active", False)):
            raise AppException(
                code=ErrorCode.AUTH_UNAUTHORIZED,
                message_key="errors.auth.account_inactive",
                status_code=401,
            )
        return user

    @staticmethod
    def _oauth_provider(provider: AuthProvider) -> OAuthProvider:
        providers: dict[AuthProvider, OAuthProvider] = {
            AuthProvider.GOOGLE: GoogleOAuthProvider(),
            AuthProvider.APPLE: AppleOAuthProvider(),
        }
        resolved = providers.get(provider)
        if resolved is None:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.invalid_oauth_provider", status_code=422)
        return resolved

    async def _allow_refresh(self, jti: str) -> None:
        try:
            await self.token_store.allow_refresh_jti(jti, ttl_days=self._refresh_ttl_days())
        except RuntimeError as exc:
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.auth.session_store_unavailable",
                status_code=503,
            ) from exc

    async def _revoke_refresh(self, jti: str) -> None:
        try:
            await self.token_store.revoke_refresh_jti(jti, ttl_days=self._refresh_ttl_days())
        except RuntimeError as exc:
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.auth.session_store_unavailable",
                status_code=503,
            ) from exc

    async def _rotate_refresh_jti_atomically(self, old_jti: str, new_jti: str) -> bool:
        try:
            return await self.token_store.rotate_refresh_jti_atomically(old_jti, new_jti, ttl_days=self._refresh_ttl_days())
        except RuntimeError as exc:
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.auth.session_store_unavailable",
                status_code=503,
            ) from exc

    async def _is_refresh_allowed(self, jti: str) -> bool:
        try:
            return await self.token_store.is_refresh_allowed(jti)
        except RuntimeError as exc:
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.auth.session_store_unavailable",
                status_code=503,
            ) from exc

    async def register(self, payload: RegisterRequest) -> tuple[object, TokenPair]:
        existing = await self.users.get_by_email(payload.email)
        if existing is not None:
            raise AppException(code=ErrorCode.CONFLICT, message_key="errors.auth.email_already_used", status_code=409)

        user = await self.users.create_user(
            email=payload.email,
            hashed_password=hash_password(payload.password.get_secret_value()),
            locale=payload.locale.value,
            timezone=payload.timezone,
        )
        await self.users.create_identity(
            user_id=user.id,
            provider=AuthProvider.LOCAL,
            provider_user_id=user.email,
            provider_email=user.email,
        )
        await self.users.get_or_create_profile(user.id)

        tokens = create_token_pair(user.id)
        refresh_payload = decode_token(tokens.refresh_token)
        await self._allow_refresh(refresh_payload.jti)
        await self.session.commit()
        return user, tokens

    async def login(self, payload: LoginRequest) -> tuple[object, TokenPair]:
        user = await self.users.get_by_email(payload.email)
        if user is None or not user.hashed_password or not verify_password(payload.password.get_secret_value(), user.hashed_password):
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.invalid_credentials", status_code=401)

        user = self._ensure_active_user(user)
        user.last_login_at = datetime.now(UTC)
        tokens = create_token_pair(user.id)
        refresh_payload = decode_token(tokens.refresh_token)
        await self._allow_refresh(refresh_payload.jti)
        await self.session.commit()
        return user, tokens

    async def refresh(self, refresh_token: str) -> TokenPair:
        try:
            payload = decode_token(refresh_token)
        except ValueError as exc:
            raise AppException(code=ErrorCode.AUTH_INVALID_TOKEN, message_key="errors.auth.invalid_token", status_code=401) from exc

        if payload.token_type.value != "refresh":
            raise AppException(code=ErrorCode.AUTH_INVALID_TOKEN, message_key="errors.auth.invalid_token_type", status_code=401)

        user = await self.users.get_by_id(payload.sub)
        self._ensure_active_user(user)

        new_pair = create_token_pair(payload.sub)
        new_payload = decode_token(new_pair.refresh_token)
        rotated = await self._rotate_refresh_jti_atomically(payload.jti, new_payload.jti)
        if not rotated:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.refresh_revoked", status_code=401)
        return new_pair

    async def logout(self, refresh_token: str | None) -> None:
        if not refresh_token:
            return
        try:
            payload = decode_token(refresh_token)
        except ValueError:
            return
        if payload.token_type.value != "refresh":
            return
        await self._revoke_refresh(payload.jti)

    async def oauth_login(self, payload: OAuthLoginRequest) -> tuple[object, TokenPair]:
        if payload.provider == AuthProvider.LOCAL:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.invalid_oauth_provider", status_code=422)
        if not payload.id_token:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.oauth_missing_token", status_code=422)

        oauth_user = await self._oauth_provider(payload.provider).resolve_user(
            code=payload.code,
            id_token=payload.id_token,
            redirect_uri=payload.redirect_uri,
        )

        identity = await self.users.get_identity(payload.provider, oauth_user.provider_user_id)
        if identity is not None:
            user = self._ensure_active_user(identity.user)
        else:
            email = oauth_user.email or f"{payload.provider.value}_{oauth_user.provider_user_id[:16]}@oauth.local"
            user = await self.users.create_user(email=email, hashed_password=None, locale="en", timezone="UTC")
            await self.users.create_identity(
                user_id=user.id,
                provider=payload.provider,
                provider_user_id=oauth_user.provider_user_id,
                provider_email=oauth_user.email,
            )
            await self.users.get_or_create_profile(user.id)

        tokens = create_token_pair(user.id)
        refresh_payload = decode_token(tokens.refresh_token)
        await self._allow_refresh(refresh_payload.jti)
        await self.session.commit()
        return user, tokens
