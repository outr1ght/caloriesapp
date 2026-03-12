class MealPlanEntity {
  const MealPlanEntity({
    required this.id,
    required this.title,
    required this.status,
    required this.planDate,
  });

  final String id;
  final String title;
  final String status;
  final DateTime planDate;
}
