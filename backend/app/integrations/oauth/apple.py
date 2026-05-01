import jwt
from jwt import InvalidTokenError

from app.common.exceptions import AppException, ErrorCode
from app.integrations.oauth.base import OAuthProvider, OAuthUserInfo


class AppleOAuthProvider(OAuthProvider):
    async def resolve_user(self, *, code: str | None, id_token: str | None, redirect_uri: str | None) -> OAuthUserInfo:
        _ = code
        _ = redirect_uri
        if not id_token:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.oauth_missing_token", status_code=422)
        try:
            claims = jwt.decode(
                id_token,
                options={
                    "verify_signature": False,
                    "verify_exp": False,
                    "verify_nbf": False,
                    "verify_iat": False,
                    "verify_aud": False,
                    "verify_iss": False,
                },
                algorithms=["HS256", "RS256", "ES256"],
            )
        except InvalidTokenError as exc:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401) from exc
        sub = str(claims.get("sub", ""))
        if not sub:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)
        return OAuthUserInfo(provider_user_id=sub, email=claims.get("email"), email_verified=bool(claims.get("email_verified", False)), display_name=None)
