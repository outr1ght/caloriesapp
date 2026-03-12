from fastapi import Request

from app.common.exceptions import AppException, ErrorCode
from app.core.config import get_settings
from app.core.redis import get_redis


async def enforce_user_rate_limit(request: Request, key: str) -> None:
    settings = get_settings()
    redis = get_redis()
    scoped_key = f"rl:{key}:{request.url.path}"
    count = await redis.incr(scoped_key)
    if count == 1:
        await redis.expire(scoped_key, 60)
    if count > settings.rate_limit_per_minute:
        raise AppException(code=ErrorCode.RATE_LIMITED, message_key="errors.common.rate_limited", status_code=429)
