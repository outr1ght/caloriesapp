from fastapi import APIRouter
from app.api.routes.v1.auth import router as auth_router
from app.api.routes.v1.me import router as me_router
from app.api.routes.v1.goals import router as goals_router
from app.api.routes.v1.settings import router as settings_router
from app.api.routes.v1.meals import router as meals_router
from app.api.routes.v1.uploads import router as uploads_router
from app.api.routes.v1.reports import router as reports_router
from app.api.routes.v1.recommendations import router as recommendations_router
from app.api.routes.v1.weights import router as weights_router
from app.api.routes.v1.barcodes import router as barcodes_router
from app.api.routes.v1.meal_plans import router as meal_plans_router
from app.api.routes.v1.localization import router as localization_router

v1_router_complete = APIRouter()
v1_router_complete.include_router(auth_router)
v1_router_complete.include_router(me_router)
v1_router_complete.include_router(goals_router)
v1_router_complete.include_router(settings_router)
v1_router_complete.include_router(meals_router)
v1_router_complete.include_router(uploads_router)
v1_router_complete.include_router(reports_router)
v1_router_complete.include_router(recommendations_router)
v1_router_complete.include_router(weights_router)
v1_router_complete.include_router(barcodes_router)
v1_router_complete.include_router(meal_plans_router)
v1_router_complete.include_router(localization_router)
