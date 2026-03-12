from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.rate_limit import enforce_user_rate_limit
from app.db.models.user import User
from app.schemas.meal_analysis import MealAnalysisRequest
from app.schemas.meals import MealCreateRequest, MealDTO, MealListQuery, MealUpdateRequest
from app.services.meal_analysis_service import MealAnalysisService
from app.services.meal_service import MealService

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("")
async def create_meal(
    payload: MealCreateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    service = MealService(session)
    meal = await service.create_meal(current_user.id, payload)
    return success_response(data=MealDTO.model_validate(meal, from_attributes=True).model_dump())


@router.get("")
async def list_meals(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> dict:
    service = MealService(session)
    items, total = await service.list_meals(current_user.id, MealListQuery(page=page, page_size=page_size))
    return success_response(
        data={
            "items": [MealDTO.model_validate(x, from_attributes=True).model_dump() for x in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@router.get("/{meal_id}")
async def get_meal(
    meal_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    service = MealService(session)
    meal = await service.get_meal(current_user.id, meal_id)
    return success_response(data=MealDTO.model_validate(meal, from_attributes=True).model_dump())


@router.patch("/{meal_id}")
async def update_meal(
    meal_id: str,
    payload: MealUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    service = MealService(session)
    meal = await service.update_meal(current_user.id, meal_id, payload)
    return success_response(data=MealDTO.model_validate(meal, from_attributes=True).model_dump())


@router.delete("/{meal_id}")
async def delete_meal(
    meal_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    service = MealService(session)
    await service.delete_meal(current_user.id, meal_id)
    return success_response(data={"deleted": True})


@router.post("/analysis")
async def analyze_meal(payload: MealAnalysisRequest, current_user: User = Depends(get_current_user)) -> dict:
    _ = current_user
    service = MealAnalysisService()
    result = await service.analyze(payload.meal_id or "ephemeral", payload.uploaded_image_ids)
    return success_response(data=result.model_dump())
