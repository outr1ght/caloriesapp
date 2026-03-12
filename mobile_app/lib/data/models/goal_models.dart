import '../../domain/entities/goal_entity.dart';

class GoalModel {
  const GoalModel({
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

  factory GoalModel.fromApi(Map<String, dynamic> root) {
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return GoalModel(
      id: (data['id'] as String?) ?? '',
      activityLevel: (data['activity_level'] as String?) ?? 'moderate',
      strategy: (data['strategy'] as String?) ?? 'maintain',
      targetCalories: _asInt(data['target_calories'], 2200),
      targetProtein: _asInt(data['target_protein_g'], 120),
      targetCarbs: _asInt(data['target_carbs_g'], 200),
      targetFat: _asInt(data['target_fat_g'], 70),
    );
  }

  GoalEntity toEntity() {
    return GoalEntity(
      id: id,
      activityLevel: activityLevel,
      strategy: strategy,
      targetCalories: targetCalories,
      targetProtein: targetProtein,
      targetCarbs: targetCarbs,
      targetFat: targetFat,
    );
  }

  static int _asInt(Object? value, int fallback) {
    if (value is num) return value.toInt();
    if (value is String) return int.tryParse(value) ?? fallback;
    return fallback;
  }
}
