from datetime import timedelta

from app.core.redis import get_redis


class TokenStore:
    PREFIX_ALLOW = "token:allow:"
    PREFIX_REVOKE = "token:revoke:"

    async def allow_refresh_jti(self, jti: str, ttl_days: int) -> None:
        redis = get_redis()
        await redis.setex(f"{self.PREFIX_ALLOW}{jti}", timedelta(days=ttl_days), "1")

    async def is_refresh_allowed(self, jti: str) -> bool:
        redis = get_redis()
        if await redis.exists(f"{self.PREFIX_REVOKE}{jti}"):
            return False
        return bool(await redis.exists(f"{self.PREFIX_ALLOW}{jti}"))

    async def revoke_refresh_jti(self, jti: str, ttl_days: int) -> None:
        redis = get_redis()
        await redis.setex(f"{self.PREFIX_REVOKE}{jti}", timedelta(days=ttl_days), "1")
        await redis.delete(f"{self.PREFIX_ALLOW}{jti}")
