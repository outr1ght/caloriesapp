class MealAnalysisItemEntity {
  const MealAnalysisItemEntity({
    required this.name,
    required this.quantity,
    required this.unit,
    required this.confidence,
  });

  final String name;
  final double quantity;
  final String unit;
  final double confidence;

  MealAnalysisItemEntity copyWith({String? name, double? quantity, String? unit, double? confidence}) {
    return MealAnalysisItemEntity(
      name: name ?? this.name,
      quantity: quantity ?? this.quantity,
      unit: unit ?? this.unit,
      confidence: confidence ?? this.confidence,
    );
  }
}

class MealAnalysisEntity {
  const MealAnalysisEntity({
    required this.mealId,
    required this.status,
    required this.items,
    required this.calories,
    required this.protein,
    required this.carbs,
    required this.fat,
    required this.confidence,
    required this.explanation,
    required this.warnings,
  });

  final String mealId;
  final String status;
  final List<MealAnalysisItemEntity> items;
  final double calories;
  final double protein;
  final double carbs;
  final double fat;
  final double confidence;
  final String explanation;
  final List<String> warnings;

  MealAnalysisEntity copyWith({List<MealAnalysisItemEntity>? items}) {
    return MealAnalysisEntity(
      mealId: mealId,
      status: status,
      items: items ?? this.items,
      calories: calories,
      protein: protein,
      carbs: carbs,
      fat: fat,
      confidence: confidence,
      explanation: explanation,
      warnings: warnings,
    );
  }
}
