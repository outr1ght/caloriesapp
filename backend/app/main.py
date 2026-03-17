from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# When this file is launched directly, prefer local backend package over similarly
# named third-party packages by inserting backend root at sys.path[0].
if __package__ in {None, ""}:
    backend_root = Path(__file__).resolve().parents[1]
    backend_root_str = str(backend_root)
    if backend_root_str not in sys.path:
        sys.path.insert(0, backend_root_str)

from app.api.router_complete import api_router_complete
from app.common.exceptions import AppException, app_exception_handler, generic_exception_handler, validation_exception_handler
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.redis import close_redis, get_redis

settings = get_settings()
configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_client = get_redis()
    try:
        await redis_client.ping()
    except Exception:
        pass
    yield
    await close_redis()


app = FastAPI(title=settings.project_name, debug=settings.debug, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept-Language", "X-Request-ID"],
)
app.include_router(api_router_complete, prefix=settings.api_v1_prefix)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


def main() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
