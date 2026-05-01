import '../../domain/entities/meal_entity.dart';

class MealModel {
  const MealModel({
    required this.id,
    required this.title,
    required this.calories,
    required this.loggedAt,
    required this.mealType,
  });

  final String id;
  final String title;
  final double calories;
  final DateTime loggedAt;
  final String mealType;

  factory MealModel.fromJson(Map<String, dynamic> json) {
    final nutrition = (json['nutrition'] as Map<String, dynamic>?) ?? const {};
    final title = ((json['title'] as String?) ?? '').trim();
    return MealModel(
      id: (json['id'] as String?) ?? '',
      title: title.isEmpty ? ((json['meal_type'] as String?) ?? '') : title,
      calories: _asDouble(nutrition['calories']),
      loggedAt: DateTime.tryParse((json['eaten_at'] as String?) ?? '')?.toUtc() ?? DateTime.now().toUtc(),
      mealType: (json['meal_type'] as String?) ?? 'meal',
    );
  }

  MealEntity toEntity() {
    return MealEntity(
      id: id,
      title: title,
      calories: calories,
      date: loggedAt,
      mealType: mealType,
    );
  }

  static double _asDouble(Object? value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value) ?? 0;
    return 0;
  }
}
