import '../../domain/entities/nutrition_report_entity.dart';

class NutritionReportModel {
  const NutritionReportModel({
    required this.totalCalories,
    required this.averageCalories,
    required this.protein,
    required this.carbs,
    required this.fat,
    required this.trend,
  });

  final double totalCalories;
  final double averageCalories;
  final double protein;
  final double carbs;
  final double fat;
  final List<ReportPointEntity> trend;

  factory NutritionReportModel.fromApi(Map<String, dynamic> root) {
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    final days = (data['days'] as List<dynamic>? ?? const [])
        .whereType<Map<String, dynamic>>()
        .toList();

    final trend = days
        .map(
          (d) => ReportPointEntity(
            label: (d['date'] as String?) ?? '',
            calories: ((d['calories'] as num?) ?? 0).toDouble(),
          ),
        )
        .toList();

    double protein = 0;
    double carbs = 0;
    double fat = 0;
    for (final d in days) {
      final macros = (d['macros'] as Map<String, dynamic>?) ?? const {};
      protein += ((macros['protein_g'] as num?) ?? 0).toDouble();
      carbs += ((macros['carbs_g'] as num?) ?? 0).toDouble();
      fat += ((macros['fat_g'] as num?) ?? 0).toDouble();
    }

    return NutritionReportModel(
      totalCalories: ((data['totals_calories'] as num?) ?? 0).toDouble(),
      averageCalories: ((data['avg_daily_calories'] as num?) ?? 0).toDouble(),
      protein: protein,
      carbs: carbs,
      fat: fat,
      trend: trend,
    );
  }

  NutritionReportEntity toEntity() {
    return NutritionReportEntity(
      totalCalories: totalCalories,
      averageCalories: averageCalories,
      protein: protein,
      carbs: carbs,
      fat: fat,
      trend: trend,
    );
  }
}
