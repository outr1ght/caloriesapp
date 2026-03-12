from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from app.schemas.meals import NutritionValueDTO

@dataclass(slots=True)
class NutritionAccumulator:
    calories: Decimal = Decimal("0")
    protein_g: Decimal = Decimal("0")
    carbs_g: Decimal = Decimal("0")
    fat_g: Decimal = Decimal("0")
    fiber_g: Decimal = Decimal("0")
    sugar_g: Decimal = Decimal("0")
    sodium_mg: Decimal = Decimal("0")

    def add(self, n: NutritionValueDTO) -> None:
        self.calories += n.calories
        self.protein_g += n.protein_g
        self.carbs_g += n.carbs_g
        self.fat_g += n.fat_g
        self.fiber_g += n.fiber_g
        self.sugar_g += n.sugar_g
        self.sodium_mg += n.sodium_mg

    def to_dto(self) -> NutritionValueDTO:
        q = lambda v: v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return NutritionValueDTO(calories=q(self.calories), protein_g=q(self.protein_g), carbs_g=q(self.carbs_g), fat_g=q(self.fat_g), fiber_g=q(self.fiber_g), sugar_g=q(self.sugar_g), sodium_mg=q(self.sodium_mg), source="deterministic", confidence=Decimal("1.000"))

class NutritionCalculationService:
    @staticmethod
    def aggregate(items: list[NutritionValueDTO]) -> NutritionValueDTO:
        acc = NutritionAccumulator()
        for item in items:
            acc.add(item)
        return acc.to_dto()
