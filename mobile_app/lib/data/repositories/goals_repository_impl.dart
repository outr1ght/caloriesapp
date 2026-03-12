import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/goal_entity.dart';
import '../../domain/repositories/goals_repository.dart';
import '../datasources/goals_api_datasource.dart';
import '../models/goal_models.dart';

final goalsApiDatasourceProvider = Provider<GoalsApiDatasource>((ref) {
  return GoalsApiDatasource(ref.read(apiClientProvider));
});

final goalsRepositoryProvider = Provider<GoalsRepository>((ref) {
  return GoalsRepositoryImpl(ref.read(goalsApiDatasourceProvider));
});

class GoalsRepositoryImpl implements GoalsRepository {
  GoalsRepositoryImpl(this._datasource);

  final GoalsApiDatasource _datasource;

  @override
  Future<GoalEntity?> getActiveGoal() async {
    final root = await _datasource.getActive();
    final data = root['data'];
    if (data == null) return null;
    if (data is! Map<String, dynamic>) return null;
    return GoalModel.fromApi(root).toEntity();
  }

  @override
  Future<bool> hasActiveGoal() async {
    final goal = await getActiveGoal();
    return goal != null && goal.targetCalories > 0;
  }

  @override
  Future<GoalEntity> saveGoal(GoalEntity goal) async {
    final active = await getActiveGoal();

    if (active != null && active.id.isNotEmpty) {
      final root = await _datasource.update(active.id, {
        'strategy': goal.strategy,
        'activity_level': goal.activityLevel,
        'target_calories': goal.targetCalories,
        'target_protein_g': goal.targetProtein,
        'target_carbs_g': goal.targetCarbs,
        'target_fat_g': goal.targetFat,
      });
      return GoalModel.fromApi(root).toEntity();
    }

    final root = await _datasource.create({
      'strategy': goal.strategy,
      'activity_level': goal.activityLevel,
      'target_calories': goal.targetCalories,
      'target_protein_g': goal.targetProtein,
      'target_carbs_g': goal.targetCarbs,
      'target_fat_g': goal.targetFat,
      'effective_from': DateTime.now().toUtc().toIso8601String(),
    });

    return GoalModel.fromApi(root).toEntity();
  }
}
