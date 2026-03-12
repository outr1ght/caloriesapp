from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import AppException, ErrorCode
from app.db.models.meal import Meal, MealItem
from app.db.models.nutrition import NutritionValue
from app.repositories.meal_repository import MealRepository
from app.schemas.meals import MealCreateRequest, MealListQuery, MealUpdateRequest
from app.services.nutrition_calculation_service import NutritionCalculationService

class MealService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = MealRepository(session)

    async def create_meal(self, user_id: str, payload: MealCreateRequest) -> Meal:
        meal = Meal(user_id=user_id, title=payload.title, notes=payload.notes, meal_type=payload.meal_type, source=payload.source, eaten_at=payload.eaten_at)
        await self.repo.create_meal(meal)
        nutrition_inputs = []
        for item in payload.items:
            nv = None
            if item.nutrition is not None:
                nv = NutritionValue(calories=item.nutrition.calories, protein_g=item.nutrition.protein_g, carbs_g=item.nutrition.carbs_g, fat_g=item.nutrition.fat_g, fiber_g=item.nutrition.fiber_g, sugar_g=item.nutrition.sugar_g, sodium_mg=item.nutrition.sodium_mg, serving_size_g=item.nutrition.serving_size_g, source=item.nutrition.source, confidence=item.nutrition.confidence)
                self.session.add(nv)
                await self.session.flush()
                nutrition_inputs.append(item.nutrition)
            await self.repo.add_item(MealItem(meal_id=meal.id, ingredient_id=item.ingredient_id, food_product_id=item.food_product_id, nutrition_value_id=nv.id if nv else None, display_name=item.display_name, quantity=item.quantity, unit=item.unit, position=item.position))
        if nutrition_inputs:
            aggregate = NutritionCalculationService.aggregate(nutrition_inputs)
            total_nv = NutritionValue(calories=aggregate.calories, protein_g=aggregate.protein_g, carbs_g=aggregate.carbs_g, fat_g=aggregate.fat_g, fiber_g=aggregate.fiber_g, sugar_g=aggregate.sugar_g, sodium_mg=aggregate.sodium_mg, source="deterministic", confidence=aggregate.confidence)
            self.session.add(total_nv)
            await self.session.flush()
            meal.nutrition_value_id = total_nv.id
        await self.session.commit()
        reloaded = await self.repo.get_meal(user_id, meal.id)
        if reloaded is None:
            raise AppException(code=ErrorCode.INTERNAL_ERROR, message_key="errors.meals.create_failed", status_code=500)
        return reloaded

    async def get_meal(self, user_id: str, meal_id: str) -> Meal:
        meal = await self.repo.get_meal(user_id, meal_id)
        if meal is None:
            raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.meals.not_found", status_code=404)
        return meal

    async def list_meals(self, user_id: str, query: MealListQuery) -> tuple[list[Meal], int]:
        return await self.repo.list_meals(user_id=user_id, page=query.page, page_size=query.page_size, from_dt=query.from_dt, to_dt=query.to_dt)

    async def update_meal(self, user_id: str, meal_id: str, payload: MealUpdateRequest) -> Meal:
        meal = await self.get_meal(user_id, meal_id)
        for k, v in payload.model_dump(exclude_none=True).items():
            setattr(meal, k, v)
        await self.session.commit()
        await self.session.refresh(meal)
        return meal

    async def delete_meal(self, user_id: str, meal_id: str) -> None:
        meal = await self.get_meal(user_id, meal_id)
        meal.mark_deleted()
        await self.session.commit()
