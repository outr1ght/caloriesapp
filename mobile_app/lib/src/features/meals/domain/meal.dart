import 'meal_item.dart';

class NutritionTotals {
  const NutritionTotals({required this.calories, required this.proteinG, required this.fatG, required this.carbsG});

  final double calories;
  final double proteinG;
  final double fatG;
  final double carbsG;
}

class Meal {
  const Meal({required this.id, required this.mealType, required this.items, required this.nutrition, required this.consumedAt});

  final String id;
  final String mealType;
  final List<MealItem> items;
  final NutritionTotals nutrition;
  final DateTime consumedAt;
}
