from datetime import timedelta

from redis.exceptions import RedisError

from app.core.redis import get_redis

_ROTATE_REFRESH_SCRIPT = """
local allow_old = KEYS[1]
local revoke_old = KEYS[2]
local allow_new = KEYS[3]
local ttl = tonumber(ARGV[1])

if redis.call('EXISTS', revoke_old) == 1 then
    return 0
end

if redis.call('EXISTS', allow_old) == 0 then
    return 0
end

redis.call('SETEX', revoke_old, ttl, '1')
redis.call('DEL', allow_old)
redis.call('SETEX', allow_new, ttl, '1')
return 1
"""


class TokenStore:
    PREFIX_ALLOW = "token:allow:"
    PREFIX_REVOKE = "token:revoke:"

    @staticmethod
    def _ttl_seconds(ttl_days: int) -> int:
        return int(timedelta(days=ttl_days).total_seconds())

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

    async def rotate_refresh_jti_atomically(self, old_jti: str, new_jti: str, ttl_days: int) -> bool:
        redis = get_redis()
        try:
            result = await redis.eval(
                _ROTATE_REFRESH_SCRIPT,
                3,
                f"{self.PREFIX_ALLOW}{old_jti}",
                f"{self.PREFIX_REVOKE}{old_jti}",
                f"{self.PREFIX_ALLOW}{new_jti}",
                str(self._ttl_seconds(ttl_days)),
            )
            return bool(result)
        except RedisError as exc:
            raise RuntimeError("token_store_unavailable") from exc

    async def revoke_refresh_jti(self, jti: str, ttl_days: int) -> None:
        redis = get_redis()
        try:
            await redis.setex(f"{self.PREFIX_REVOKE}{jti}", timedelta(days=ttl_days), "1")
            await redis.delete(f"{self.PREFIX_ALLOW}{jti}")
        except RedisError as exc:
            raise RuntimeError("token_store_unavailable") from exc
