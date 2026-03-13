from datetime import timedelta

from redis.exceptions import RedisError

from app.core.redis import get_redis


class TokenStore:
    PREFIX_ALLOW = "token:allow:"
    PREFIX_REVOKE = "token:revoke:"

    async def allow_refresh_jti(self, jti: str, ttl_days: int) -> None:
        redis = get_redis()
        try:
            await redis.setex(f"{self.PREFIX_ALLOW}{jti}", timedelta(days=ttl_days), "1")
        except RedisError as exc:
            raise RuntimeError("token_store_unavailable") from exc

    async def is_refresh_allowed(self, jti: str) -> bool:
        redis = get_redis()
        try:
            if await redis.exists(f"{self.PREFIX_REVOKE}{jti}"):
                return False
            return bool(await redis.exists(f"{self.PREFIX_ALLOW}{jti}"))
        except RedisError as exc:
            raise RuntimeError("token_store_unavailable") from exc

    async def revoke_refresh_jti(self, jti: str, ttl_days: int) -> None:
        redis = get_redis()
        try:
            await redis.setex(f"{self.PREFIX_REVOKE}{jti}", timedelta(days=ttl_days), "1")
            await redis.delete(f"{self.PREFIX_ALLOW}{jti}")
        except RedisError as exc:
            raise RuntimeError("token_store_unavailable") from exc
