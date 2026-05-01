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
            calories: _asDouble(d['calories']),
          ),
        )
        .toList();

    double protein = 0;
    double carbs = 0;
    double fat = 0;
    for (final d in days) {
      final macros = (d['macros'] as Map<String, dynamic>?) ?? const {};
      protein += _asDouble(macros['protein_g']);
      carbs += _asDouble(macros['carbs_g']);
      fat += _asDouble(macros['fat_g']);
    }

    return NutritionReportModel(
      totalCalories: _asDouble(data['totals_calories']),
      averageCalories: _asDouble(data['avg_daily_calories']),
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

  static double _asDouble(Object? value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value) ?? 0;
    return 0;
  }
}
