from types import SimpleNamespace

import pytest
from redis.exceptions import RedisError
from starlette.requests import Request

from app.common.exceptions import AppException, ErrorCode
from app.core.rate_limit import enforce_user_rate_limit


class FakeRedis:
    def __init__(self, *, count=1, error: Exception | None = None):
        self.count = count
        self.error = error
        self.expire_calls = []

    async def incr(self, key: str) -> int:
        if self.error is not None:
            raise self.error
        self.last_key = key
        return self.count

    async def expire(self, key: str, ttl: int) -> None:
        self.expire_calls.append((key, ttl))


def make_request(path: str = "/api/v1/meals/analysis", request_id: str = "req-123") -> Request:
    scope = {
        "type": "http",
        "method": "POST",
        "path": path,
        "headers": [],
        "client": ("127.0.0.1", 50000),
        "scheme": "http",
        "server": ("testserver", 80),
        "query_string": b"",
    }
    request = Request(scope)
    request.state.request_id = request_id
    return request


@pytest.mark.asyncio
async def test_rate_limit_allows_request_under_limit(monkeypatch):
    fake_redis = FakeRedis(count=1)
    fake_settings = SimpleNamespace(
        rate_limit_per_minute=120,
        rate_limit_auth_per_minute=30,
        rate_limit_meal_analysis_per_minute=20,
        rate_limit_uploads_per_minute=40,
    )
    monkeypatch.setattr("app.core.rate_limit.get_redis", lambda: fake_redis)
    monkeypatch.setattr("app.core.rate_limit.get_settings", lambda: fake_settings)

    await enforce_user_rate_limit(make_request(), "user:1", category="meal_analysis", user_id="user-1")

    assert fake_redis.expire_calls == [("rl:meal_analysis:user:1:/api/v1/meals/analysis", 60)]


@pytest.mark.asyncio
async def test_rate_limit_blocks_request_over_limit(monkeypatch, caplog):
    fake_redis = FakeRedis(count=21)
    fake_settings = SimpleNamespace(
        rate_limit_per_minute=120,
        rate_limit_auth_per_minute=30,
        rate_limit_meal_analysis_per_minute=20,
        rate_limit_uploads_per_minute=40,
    )
    monkeypatch.setattr("app.core.rate_limit.get_redis", lambda: fake_redis)
    monkeypatch.setattr("app.core.rate_limit.get_settings", lambda: fake_settings)

    with pytest.raises(AppException) as exc:
        await enforce_user_rate_limit(make_request(), "user:1", category="meal_analysis", user_id="user-1")

    assert exc.value.code == ErrorCode.RATE_LIMITED
    assert exc.value.status_code == 429
    assert any(getattr(record, "event", {}).get("event_name") == "rate_limit_exceeded" for record in caplog.records)


@pytest.mark.asyncio
async def test_rate_limit_redis_unavailable_allows_request_and_logs(monkeypatch, caplog):
    fake_redis = FakeRedis(error=RedisError("redis down"))
    fake_settings = SimpleNamespace(
        rate_limit_per_minute=120,
        rate_limit_auth_per_minute=30,
        rate_limit_meal_analysis_per_minute=20,
        rate_limit_uploads_per_minute=40,
    )
    monkeypatch.setattr("app.core.rate_limit.get_redis", lambda: fake_redis)
    monkeypatch.setattr("app.core.rate_limit.get_settings", lambda: fake_settings)

    await enforce_user_rate_limit(make_request(path="/api/v1/uploads/init"), "user:1", category="uploads", user_id="user-1")

    degraded_events = [getattr(record, "event", {}) for record in caplog.records if getattr(record, "event", {}).get("event_name") == "rate_limiter_degraded"]
    assert degraded_events
    assert degraded_events[0]["category"] == "uploads"
    assert degraded_events[0]["user_id"] == "user-1"
