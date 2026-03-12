from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Ingredient, NutritionValue


def run() -> None:
    db: Session = SessionLocal()
    try:
        chicken = Ingredient(canonical_name='chicken breast', display_name='Chicken Breast')
        rice = Ingredient(canonical_name='rice', display_name='Rice')
        db.add_all([chicken, rice])
        db.flush()
        db.add_all([
            NutritionValue(ingredient_id=chicken.id, calories_per_100g=165, protein_per_100g=31, fat_per_100g=3.6, carbs_per_100g=0),
            NutritionValue(ingredient_id=rice.id, calories_per_100g=130, protein_per_100g=2.7, fat_per_100g=0.3, carbs_per_100g=28),
        ])
        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    run()
