from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class MacroBreakdownDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    protein_g: Decimal
    carbs_g: Decimal
    fat_g: Decimal


class DailyNutritionSummaryDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    date: date
    calories: Decimal
    macros: MacroBreakdownDTO
    meal_count: int


class NutritionReportDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    date_from: date
    date_to: date
    totals_calories: Decimal
    avg_daily_calories: Decimal
    days: list[DailyNutritionSummaryDTO]
