import '../../domain/entities/meal_entity.dart';

class MealModel {
  const MealModel({required this.id, required this.title, required this.calories, required this.loggedAt});

  final String id;
  final String title;
  final double calories;
  final DateTime loggedAt;

  factory MealModel.fromJson(Map<String, dynamic> json) {
    final nutrition = (json['nutrition'] as Map<String, dynamic>?) ?? const {};
    return MealModel(
      id: (json['id'] as String?) ?? '',
      title: (json['meal_type'] as String?) ?? '',
      calories: ((nutrition['calories'] as num?) ?? 0).toDouble(),
      loggedAt: DateTime.tryParse((json['logged_at'] as String?) ?? '')?.toUtc() ?? DateTime.now().toUtc(),
    );
  }

  MealEntity toEntity() {
    return MealEntity(id: id, title: title, calories: calories, date: loggedAt);
  }
}
