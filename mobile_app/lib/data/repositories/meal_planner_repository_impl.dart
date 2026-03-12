import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/meal_plan_entity.dart';
import '../../domain/repositories/meal_planner_repository.dart';
import '../datasources/meal_plans_api_datasource.dart';
import '../models/meal_plan_models.dart';

final mealPlansApiDatasourceProvider = Provider<MealPlansApiDatasource>((ref) {
  return MealPlansApiDatasource(ref.read(apiClientProvider));
});

final mealPlannerRepositoryProvider = Provider<MealPlannerRepository>((ref) {
  return MealPlannerRepositoryImpl(ref.read(mealPlansApiDatasourceProvider));
});

class MealPlannerRepositoryImpl implements MealPlannerRepository {
  MealPlannerRepositoryImpl(this._datasource);

  final MealPlansApiDatasource _datasource;

  @override
  Future<List<MealPlanEntity>> list() async {
    final root = await _datasource.list();
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    final items = (data['items'] as List<dynamic>? ?? const []).whereType<Map<String, dynamic>>();
    return items.map((x) => MealPlanModel.fromJson(x).toEntity()).toList();
  }
}
