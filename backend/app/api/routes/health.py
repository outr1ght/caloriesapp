from fastapi import APIRouter

from app.common.responses import success_response

router = APIRouter()


@router.get("/health")
async def healthcheck() -> dict:
    return success_response(data={"status": "ok"}, message_key="messages.health.ok")
