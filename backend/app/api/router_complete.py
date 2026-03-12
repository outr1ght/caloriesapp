from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.v1.router_complete import v1_router_complete

api_router_complete = APIRouter()
api_router_complete.include_router(health_router, tags=["health"])
api_router_complete.include_router(v1_router_complete)
