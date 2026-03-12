class ReportPointEntity {
  const ReportPointEntity({required this.label, required this.calories});

  final String label;
  final double calories;
}

class NutritionReportEntity {
  const NutritionReportEntity({
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
}
