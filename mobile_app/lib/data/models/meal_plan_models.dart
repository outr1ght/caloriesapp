import '../../domain/entities/meal_plan_entity.dart';

class MealPlanModel {
  const MealPlanModel({
    required this.id,
    required this.title,
    required this.status,
    required this.planDate,
  });

  final String id;
  final String title;
  final String status;
  final DateTime planDate;

  factory MealPlanModel.fromJson(Map<String, dynamic> json) {
    return MealPlanModel(
      id: (json['id'] as String?) ?? '',
      title: (json['title'] as String?) ?? '',
      status: (json['status'] as String?) ?? 'draft',
      planDate: DateTime.tryParse((json['plan_date'] as String?) ?? '')?.toUtc() ?? DateTime.now().toUtc(),
    );
  }

  MealPlanEntity toEntity() {
    return MealPlanEntity(id: id, title: title, status: status, planDate: planDate);
  }
}
