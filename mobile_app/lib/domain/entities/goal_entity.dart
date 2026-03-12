class GoalEntity {
  const GoalEntity({
    required this.id,
    required this.activityLevel,
    required this.strategy,
    required this.targetCalories,
    required this.targetProtein,
    required this.targetCarbs,
    required this.targetFat,
  });

  final String id;
  final String activityLevel;
  final String strategy;
  final int targetCalories;
  final int targetProtein;
  final int targetCarbs;
  final int targetFat;
}
