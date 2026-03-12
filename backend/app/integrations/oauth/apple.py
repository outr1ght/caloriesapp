from jose import jwt

from app.common.exceptions import AppException, ErrorCode
from app.integrations.oauth.base import OAuthProvider, OAuthUserInfo


class AppleOAuthProvider(OAuthProvider):
    async def resolve_user(self, *, code: str | None, id_token: str | None, redirect_uri: str | None) -> OAuthUserInfo:
        _ = code
        _ = redirect_uri
        if not id_token:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.oauth_missing_token", status_code=422)
        try:
            claims = jwt.get_unverified_claims(id_token)
        except Exception as exc:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401) from exc
        sub = str(claims.get("sub", ""))
        if not sub:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)
        return OAuthUserInfo(provider_user_id=sub, email=claims.get("email"), email_verified=bool(claims.get("email_verified", False)), display_name=None)
