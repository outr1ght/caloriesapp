from datetime import datetime
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.pagination import PaginationMeta, build_paginated_data
from app.core.rate_limit import enforce_user_rate_limit
from app.core.serialization import serialize_api_data
from app.db.models.domain_enums import AnalysisStatus, MealSource, MealType, UploadStatus
from app.db.models.user import User
from app.schemas.meal_analysis import MealAnalysisRequest
from app.schemas.meals import MealCreateRequest, MealDTO, MealListQuery, MealUpdateRequest
from app.services.meal_analysis_service import MealAnalysisService
from app.services.meal_service import MealService

router = APIRouter(prefix="/meals", tags=["meals"])


class MealNutritionSummaryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    calories: Decimal = Field(ge=0)
    protein_g: Decimal = Field(ge=0)
    carbs_g: Decimal = Field(ge=0)
    fat_g: Decimal = Field(ge=0)


class MealItemReadResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    ingredient_id: str | None = None
    food_product_id: str | None = None
    display_name: str
    quantity: Decimal = Field(gt=0)
    unit: str
    position: int = Field(ge=0)


class MealImageReferenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    storage_key: str
    mime_type: str
    file_size: int = Field(ge=0)
    status: UploadStatus
    created_at: datetime


class MealReadResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    user_id: str
    title: str | None = None
    notes: str | None = None
    meal_type: MealType
    source: MealSource
    eaten_at: datetime
    analysis_status: AnalysisStatus
    nutrition_summary: MealNutritionSummaryResponse | None = None
    items: list[MealItemReadResponse] = Field(default_factory=list)
    images: list[MealImageReferenceResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class MealListDataResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[MealReadResponse]
    meta: PaginationMeta


class MealReadEnvelopeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    message_key: str
    data: MealReadResponse
    error: None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class MealListEnvelopeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    message_key: str
    data: MealListDataResponse
    error: None = None
    meta: dict[str, Any] = Field(default_factory=dict)


def _require_uuid(value: str) -> None:
    try:
        UUID(value)
    except ValueError as exc:
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.validation.invalid_uuid", status_code=422) from exc


def _serialize_meal(meal: Any) -> dict[str, Any]:
    nutrition_value = getattr(meal, "nutrition_value", None)
    nutrition_summary = None
    if nutrition_value is not None:
        nutrition_summary = MealNutritionSummaryResponse(
            calories=nutrition_value.calories,
            protein_g=nutrition_value.protein_g,
            carbs_g=nutrition_value.carbs_g,
            fat_g=nutrition_value.fat_g,
        )

    items = [
        MealItemReadResponse(
            id=item.id,
            ingredient_id=item.ingredient_id,
            food_product_id=item.food_product_id,
            display_name=item.display_name,
            quantity=item.quantity,
            unit=item.unit,
            position=item.position,
        )
        for item in (getattr(meal, "items", None) or [])
    ]
    images = [
        MealImageReferenceResponse(
            id=image.id,
            storage_key=image.storage_key,
            mime_type=image.mime_type,
            file_size=image.file_size,
            status=image.status,
            created_at=image.created_at,
        )
        for image in (getattr(meal, "uploaded_images", None) or [])
    ]
    return MealReadResponse(
        id=meal.id,
        user_id=meal.user_id,
        title=meal.title,
        notes=meal.notes,
        meal_type=meal.meal_type,
        source=meal.source,
        eaten_at=meal.eaten_at,
        analysis_status=meal.analysis_status,
        nutrition_summary=nutrition_summary,
        items=items,
        images=images,
        created_at=meal.created_at,
        updated_at=meal.updated_at,
    ).model_dump()


@router.post("")
async def create_meal(
    payload: MealCreateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}", user_id=current_user.id)
    service = MealService(session)
    meal = await service.create_meal(current_user.id, payload)
    return success_response(data=serialize_api_data(MealDTO.model_validate(meal, from_attributes=True).model_dump()))


@router.get("", response_model=MealListEnvelopeResponse)
async def list_meals(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> dict:
    service = MealService(session)
    items, total = await service.list_meals(current_user.id, MealListQuery(page=page, page_size=page_size))
    return success_response(
        data=serialize_api_data(
            build_paginated_data(
                items=[_serialize_meal(x) for x in items],
                page=page,
                page_size=page_size,
                total=total,
            )
        )
    )


@router.get("/{meal_id}", response_model=MealReadEnvelopeResponse)
async def get_meal(
    meal_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    _require_uuid(meal_id)
    service = MealService(session)
    meal = await service.get_meal(current_user.id, meal_id)
    return success_response(data=serialize_api_data(_serialize_meal(meal)))


@router.patch("/{meal_id}")
async def update_meal(
    meal_id: str,
    payload: MealUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    _require_uuid(meal_id)
    service = MealService(session)
    meal = await service.update_meal(current_user.id, meal_id, payload)
    return success_response(data=serialize_api_data(MealDTO.model_validate(meal, from_attributes=True).model_dump()))


@router.delete("/{meal_id}")
async def delete_meal(
    meal_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    _require_uuid(meal_id)
    service = MealService(session)
    await service.delete_meal(current_user.id, meal_id)
    return success_response(data={"deleted": True})


@router.post("/analysis")
async def analyze_meal(
    payload: MealAnalysisRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}", category="meal_analysis", user_id=current_user.id)
    if payload.meal_id:
        _require_uuid(payload.meal_id)
    service = MealAnalysisService()
    result = await service.analyze(payload.meal_id or "ephemeral", payload.uploaded_image_ids)
    return success_response(data=serialize_api_data(result.model_dump()))
