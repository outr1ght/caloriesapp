from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ingredient, NutritionValue


class NutritionService:
    def map_item(self, db: Session, name: str, grams: float) -> dict[str, float]:
        ingredient = db.scalar(select(Ingredient).where(Ingredient.canonical_name == name.lower()))
        if ingredient:
            nv = db.scalar(select(NutritionValue).where(NutritionValue.ingredient_id == ingredient.id))
            if nv:
                factor = grams / 100.0
                return {
                    "calories": nv.calories_per_100g * factor,
                    "protein_g": nv.protein_per_100g * factor,
                    "fat_g": nv.fat_per_100g * factor,
                    "carbs_g": nv.carbs_per_100g * factor,
                }
        return {"calories": grams * 1.6, "protein_g": grams * 0.08, "fat_g": grams * 0.05, "carbs_g": grams * 0.12}


nutrition_service = NutritionService()
