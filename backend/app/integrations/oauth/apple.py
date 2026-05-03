from jwt import InvalidTokenError, PyJWKClient
import jwt

from app.common.exceptions import AppException, ErrorCode
from app.core.config import get_settings
from app.integrations.oauth.base import OAuthProvider, OAuthUserInfo

_APPLE_ISSUER = "https://appleid.apple.com"


class AppleOAuthProvider(OAuthProvider):
    async def resolve_user(self, *, code: str | None, id_token: str | None, redirect_uri: str | None) -> OAuthUserInfo:
        _ = code
        _ = redirect_uri
        if not id_token:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.oauth_missing_token", status_code=422)

        settings = get_settings()
        if not settings.apple_oauth_client_id:
            raise AppException(code=ErrorCode.INTERNAL_ERROR, message_key="errors.common.internal", status_code=500)

        try:
            signing_key = PyJWKClient(settings.apple_oauth_jwks_url).get_signing_key_from_jwt(id_token)
            claims = jwt.decode(
                id_token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.apple_oauth_client_id,
                issuer=_APPLE_ISSUER,
            )
        except InvalidTokenError as exc:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401) from exc
        except Exception as exc:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401) from exc

        sub = str(claims.get("sub", ""))
        if not sub:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)
        return OAuthUserInfo(
            provider_user_id=sub,
            email=claims.get("email"),
            email_verified=str(claims.get("email_verified", "false")).lower() == "true",
            display_name=None,
        )
