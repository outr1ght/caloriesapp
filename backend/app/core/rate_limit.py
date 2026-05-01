from typing import Literal

from fastapi import Request
from redis.exceptions import RedisError

from app.common.exceptions import AppException, ErrorCode
from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.core.redis import get_redis

logger = get_logger(__name__)
RateLimitCategory = Literal["default", "auth", "meal_analysis", "uploads"]


def _resolve_limit(settings: Settings, category: RateLimitCategory) -> int:
    category_limits = {
        "default": settings.rate_limit_per_minute,
        "auth": settings.rate_limit_auth_per_minute or settings.rate_limit_per_minute,
        "meal_analysis": settings.rate_limit_meal_analysis_per_minute or settings.rate_limit_per_minute,
        "uploads": settings.rate_limit_uploads_per_minute or settings.rate_limit_per_minute,
    }
    return category_limits[category]


def _request_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


async def enforce_user_rate_limit(
    request: Request,
    key: str,
    *,
    category: RateLimitCategory = "default",
    user_id: str | None = None,
) -> None:
    settings = get_settings()
    redis = get_redis()
    limit = _resolve_limit(settings, category)
    scoped_key = f"rl:{category}:{key}:{request.url.path}"
    request_id = getattr(request.state, "request_id", None)
    ip_address = _request_ip(request)
    event = {
        "request_id": request_id,
        "user_id": user_id,
        "ip": ip_address,
        "path": request.url.path,
        "category": category,
        "limit": limit,
    }
    try:
        count = await redis.incr(scoped_key)
        if count == 1:
            await redis.expire(scoped_key, 60)
    except RedisError as exc:
        logger.warning(
            "rate limiter degraded",
            extra={"event": {**event, "event_name": "rate_limiter_degraded", "error_type": type(exc).__name__}},
        )
        return

    if count > limit:
        logger.warning(
            "rate limit exceeded",
            extra={"event": {**event, "event_name": "rate_limit_exceeded", "current_count": count}},
        )
        raise AppException(code=ErrorCode.RATE_LIMITED, message_key="errors.common.rate_limited", status_code=429)
