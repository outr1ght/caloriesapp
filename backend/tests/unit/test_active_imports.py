from app.api.router_complete import api_router_complete
from app.api.routes.health import router as health_router
from app.api.routes.v1 import auth, barcodes, goals, localization, me, meal_plans, meals, recommendations, reports, settings, uploads, weights
from app.api.routes.v1.router_complete import v1_router_complete
from app.core.database import get_engine, get_session, get_session_factory
from app.core.dependencies import bearer_scheme, db_session, get_current_user
from app.db.models import Meal, NutritionGoal, User, UserSettings
from app.main import app
from app.schemas.auth import LoginRequest, RefreshTokenRequest
from app.schemas.meals import MealCreateRequest


def test_active_startup_modules_import() -> None:
    assert app.title
    assert app.docs_url == "/docs"
    assert app.openapi_url == "/openapi.json"
    assert api_router_complete.routes
    assert v1_router_complete.routes
    assert health_router.routes


def test_active_route_modules_import() -> None:
    routers = [
        auth.router,
        barcodes.router,
        goals.router,
        localization.router,
        me.router,
        meal_plans.router,
        meals.router,
        recommendations.router,
        reports.router,
        settings.router,
        uploads.router,
        weights.router,
    ]
    assert all(router.routes for router in routers)


def test_active_models_package_exports() -> None:
    assert User.__name__ == "User"
    assert Meal.__name__ == "Meal"
    assert NutritionGoal.__name__ == "NutritionGoal"
    assert UserSettings.__name__ == "UserSettings"


def test_active_schema_modules_import() -> None:
    assert LoginRequest.model_fields
    assert RefreshTokenRequest.model_fields
    assert MealCreateRequest.model_fields


def test_database_startup_helpers_import() -> None:
    assert callable(get_engine)
    assert callable(get_session_factory)
    assert callable(get_session)


def test_auth_dependency_exports_import() -> None:
    assert bearer_scheme is not None
    assert callable(db_session)
    assert callable(get_current_user)
