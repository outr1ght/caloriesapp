from fastapi import APIRouter

from app.api.v1.endpoints import auth, me, uploads, meals, reports, recommendations, weights, barcodes, meal_plans, localization

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(me.router, tags=["me"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(meals.router, prefix="/meals", tags=["meals"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(weights.router, prefix="/weights", tags=["weights"])
api_router.include_router(barcodes.router, prefix="/barcodes", tags=["barcodes"])
api_router.include_router(meal_plans.router, prefix="/meal-plans", tags=["meal-plans"])
api_router.include_router(localization.router, prefix="/localization", tags=["localization"])
