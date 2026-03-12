import '../../domain/entities/meal_analysis_entity.dart';

class MealAnalysisModel {
  const MealAnalysisModel({
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

  factory MealAnalysisModel.fromApi(Map<String, dynamic> root) {
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    final nutrition = (data['estimated_nutrition'] as Map<String, dynamic>?) ?? const {};

    final items = (data['items'] as List<dynamic>? ?? const [])
        .whereType<Map<String, dynamic>>()
        .map(
          (x) => MealAnalysisItemEntity(
            name: (x['name'] as String?) ?? '',
            quantity: ((x['estimated_quantity'] as num?) ?? 0).toDouble(),
            unit: (x['unit'] as String?) ?? 'g',
            confidence: ((x['confidence'] as num?) ?? 0).toDouble(),
          ),
        )
        .toList();

    return MealAnalysisModel(
      mealId: (data['meal_id'] as String?) ?? '',
      status: (data['status'] as String?) ?? 'ready',
      items: items,
      calories: ((nutrition['calories'] as num?) ?? 0).toDouble(),
      protein: ((nutrition['protein_g'] as num?) ?? 0).toDouble(),
      carbs: ((nutrition['carbs_g'] as num?) ?? 0).toDouble(),
      fat: ((nutrition['fat_g'] as num?) ?? 0).toDouble(),
      confidence: ((nutrition['confidence'] as num?) ?? 0).toDouble(),
      explanation: (data['explanation'] as String?) ?? '',
      warnings: (data['warnings'] as List<dynamic>? ?? const []).map((e) => e.toString()).toList(),
    );
  }

  MealAnalysisEntity toEntity() {
    return MealAnalysisEntity(
      mealId: mealId,
      status: status,
      items: items,
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
