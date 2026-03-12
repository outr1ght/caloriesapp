from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Ingredient, Meal, MealItem
from app.db.models.enums import MealType


class MealRepository:
    def _map_meal_type(self, meal_type: str) -> MealType:
        return MealType(meal_type)

    def list_by_user(self, db: Session, user_id: str, page: int, page_size: int) -> tuple[list[Meal], int]:
        offset = (page - 1) * page_size

        total_stmt = select(func.count()).select_from(Meal).where(Meal.user_id == user_id, Meal.deleted_at.is_(None))
        total_items = int(db.scalar(total_stmt) or 0)

        items_stmt = (
            select(Meal)
            .where(Meal.user_id == user_id, Meal.deleted_at.is_(None))
            .order_by(Meal.consumed_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        meals = list(db.scalars(items_stmt))
        return meals, total_items

    def get_by_id(self, db: Session, user_id: str, meal_id: str) -> Meal | None:
        return db.scalar(select(Meal).where(Meal.id == meal_id, Meal.user_id == user_id, Meal.deleted_at.is_(None)))

    def get_items(self, db: Session, meal_id: str) -> list[MealItem]:
        return list(db.scalars(select(MealItem).where(MealItem.meal_id == meal_id, MealItem.deleted_at.is_(None))))

    def _get_or_create_ingredient(self, db: Session, name: str) -> Ingredient:
        canonical = name.strip().lower()
        ingredient = db.scalar(select(Ingredient).where(Ingredient.canonical_name == canonical))
        if ingredient:
            return ingredient

        ingredient = Ingredient(canonical_name=canonical, display_name=name.strip())
        db.add(ingredient)
        db.flush()
        return ingredient

    def create(
        self,
        db: Session,
        user_id: str,
        meal_type: str,
        consumed_at: datetime,
        image_id: str | None,
        analysis_confidence: float | None,
        item_payloads: list[dict],
    ) -> Meal:
        meal = Meal(
            user_id=user_id,
            meal_type=self._map_meal_type(meal_type),
            consumed_at=consumed_at,
            image_id=image_id,
            analysis_confidence=analysis_confidence,
        )
        db.add(meal)
        db.flush()

        for item in item_payloads:
            ingredient = self._get_or_create_ingredient(db, item["name"])
            db_item = MealItem(
                meal_id=meal.id,
                ingredient_id=ingredient.id,
                name=item["name"],
                grams=item["grams"],
                confidence=item.get("confidence"),
                calories=item["calories"],
                protein_g=item["protein_g"],
                fat_g=item["fat_g"],
                carbs_g=item["carbs_g"],
            )
            db.add(db_item)

        db.flush()
        return meal

    def replace_items(self, db: Session, meal: Meal, item_payloads: list[dict]) -> None:
        now = datetime.now(timezone.utc)
        existing_items = self.get_items(db, meal.id)
        for old_item in existing_items:
            old_item.deleted_at = now

        for item in item_payloads:
            ingredient = self._get_or_create_ingredient(db, item["name"])
            db_item = MealItem(
                meal_id=meal.id,
                ingredient_id=ingredient.id,
                name=item["name"],
                grams=item["grams"],
                confidence=item.get("confidence"),
                calories=item["calories"],
                protein_g=item["protein_g"],
                fat_g=item["fat_g"],
                carbs_g=item["carbs_g"],
            )
            db.add(db_item)

    def soft_delete(self, db: Session, meal: Meal) -> None:
        meal.deleted_at = datetime.now(timezone.utc)


meal_repository = MealRepository()
