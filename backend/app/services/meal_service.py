from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.enums import MealType
from app.db.repositories.meal_repository import meal_repository
from app.schemas.common import build_pagination_meta
from app.schemas.meal import MealCreateRequest, MealItemIn, MealListResponse, MealPatchRequest, MealResponse, NutritionTotals
from app.services.nutrition.nutrition_service import nutrition_service


class MealService:
    def _map_items_with_nutrition(self, db: Session, items: list[MealItemIn]) -> tuple[list[dict], NutritionTotals]:
        payloads: list[dict] = []
        totals = {"calories": 0.0, "protein_g": 0.0, "fat_g": 0.0, "carbs_g": 0.0}

        for item in items:
            mapped = nutrition_service.map_item(db, item.name, item.grams)
            totals["calories"] += mapped["calories"]
            totals["protein_g"] += mapped["protein_g"]
            totals["fat_g"] += mapped["fat_g"]
            totals["carbs_g"] += mapped["carbs_g"]

            payloads.append(
                {
                    "name": item.name,
                    "grams": item.grams,
                    "confidence": item.confidence,
                    "calories": mapped["calories"],
                    "protein_g": mapped["protein_g"],
                    "fat_g": mapped["fat_g"],
                    "carbs_g": mapped["carbs_g"],
                }
            )

        return payloads, NutritionTotals(**totals)

    def _meal_to_response(self, db: Session, meal) -> MealResponse:
        db_items = meal_repository.get_items(db, meal.id)
        response_items = [MealItemIn(name=i.name, grams=float(i.grams), confidence=i.confidence) for i in db_items]

        totals = {
            "calories": float(sum(i.calories for i in db_items)),
            "protein_g": float(sum(i.protein_g for i in db_items)),
            "fat_g": float(sum(i.fat_g for i in db_items)),
            "carbs_g": float(sum(i.carbs_g for i in db_items)),
        }

        return MealResponse(
            meal_id=meal.id,
            meal_type=meal.meal_type.value,
            consumed_at=meal.consumed_at,
            items=response_items,
            nutrition=NutritionTotals(**totals),
        )

    def create_meal(self, db: Session, user_id: str, payload: MealCreateRequest) -> MealResponse:
        item_payloads, totals = self._map_items_with_nutrition(db, payload.items)
        meal = meal_repository.create(
            db=db,
            user_id=user_id,
            meal_type=payload.meal_type,
            consumed_at=payload.consumed_at,
            image_id=payload.image_id,
            analysis_confidence=None,
            item_payloads=item_payloads,
        )
        db.commit()
        db.refresh(meal)

        return MealResponse(
            meal_id=meal.id,
            meal_type=meal.meal_type.value,
            consumed_at=meal.consumed_at,
            items=payload.items,
            nutrition=totals,
        )

    def list_meals(self, db: Session, user_id: str, page: int, page_size: int) -> MealListResponse:
        meals, total_items = meal_repository.list_by_user(db, user_id, page=page, page_size=page_size)
        items = [self._meal_to_response(db, meal) for meal in meals]
        meta = build_pagination_meta(page=page, page_size=page_size, total_items=total_items)
        return MealListResponse(items=items, pagination=meta)

    def get_meal(self, db: Session, user_id: str, meal_id: str) -> MealResponse:
        meal = meal_repository.get_by_id(db, user_id, meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")
        return self._meal_to_response(db, meal)

    def patch_meal(self, db: Session, user_id: str, meal_id: str, payload: MealPatchRequest) -> MealResponse:
        meal = meal_repository.get_by_id(db, user_id, meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")

        item_payloads, totals = self._map_items_with_nutrition(db, payload.items)
        meal.meal_type = MealType(payload.meal_type)
        meal.consumed_at = payload.consumed_at
        meal.image_id = payload.image_id
        meal_repository.replace_items(db, meal, item_payloads)
        db.commit()
        db.refresh(meal)

        return MealResponse(
            meal_id=meal.id,
            meal_type=meal.meal_type.value,
            consumed_at=meal.consumed_at,
            items=payload.items,
            nutrition=totals,
        )

    def delete_meal(self, db: Session, user_id: str, meal_id: str) -> None:
        meal = meal_repository.get_by_id(db, user_id, meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")

        meal_repository.soft_delete(db, meal)
        db.commit()


meal_service = MealService()
