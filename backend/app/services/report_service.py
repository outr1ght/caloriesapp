from collections import defaultdict
from datetime import UTC, date, datetime, time
from decimal import Decimal
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.models.meal import Meal
from app.schemas.reports import DailyNutritionSummaryDTO, MacroBreakdownDTO, NutritionReportDTO

class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def nutrition_report(self, user_id: str, date_from: date, date_to: date) -> NutritionReportDTO:
        from_dt = datetime.combine(date_from, time.min, tzinfo=UTC)
        to_dt = datetime.combine(date_to, time.max, tzinfo=UTC)
        result = await self.session.execute(select(Meal).where(and_(Meal.user_id == user_id, Meal.deleted_at.is_(None), Meal.eaten_at >= from_dt, Meal.eaten_at <= to_dt)).options(selectinload(Meal.nutrition_value)))
        meals = list(result.scalars().all())
        per_day = defaultdict(lambda: {"calories": Decimal("0"), "protein_g": Decimal("0"), "carbs_g": Decimal("0"), "fat_g": Decimal("0"), "meal_count": 0})
        total_calories = Decimal("0")
        for meal in meals:
            if meal.nutrition_value is None:
                continue
            d = meal.eaten_at.date()
            p = per_day[d]
            p["calories"] += meal.nutrition_value.calories
            p["protein_g"] += meal.nutrition_value.protein_g
            p["carbs_g"] += meal.nutrition_value.carbs_g
            p["fat_g"] += meal.nutrition_value.fat_g
            p["meal_count"] += 1
            total_calories += meal.nutrition_value.calories
        day_count = max((date_to - date_from).days + 1, 1)
        avg_daily = (total_calories / Decimal(day_count)).quantize(Decimal("0.01"))
        days = [DailyNutritionSummaryDTO(date=d, calories=p["calories"].quantize(Decimal("0.01")), macros=MacroBreakdownDTO(protein_g=p["protein_g"].quantize(Decimal("0.01")), carbs_g=p["carbs_g"].quantize(Decimal("0.01")), fat_g=p["fat_g"].quantize(Decimal("0.01"))), meal_count=int(p["meal_count"])) for d, p in sorted(per_day.items())]
        return NutritionReportDTO(date_from=date_from, date_to=date_to, totals_calories=total_calories.quantize(Decimal("0.01")), avg_daily_calories=avg_daily, days=days)
