import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/storage/local_cache.dart';
import '../../profile_setup/data/local_profile_setup_repository.dart';
import '../domain/calorie_goal.dart';
import '../domain/calorie_goal_repository.dart';

final calorieGoalRepositoryProvider = Provider<CalorieGoalRepository>((ref) {
  return LocalCalorieGoalRepository(ref.read(localCacheProvider));
});

class LocalCalorieGoalRepository implements CalorieGoalRepository {
  LocalCalorieGoalRepository(this._cache);

  final LocalCache _cache;
  static const _key = 'calorie_goal_v1';

  @override
  Future<CalorieGoal?> load() async {
    final json = await _cache.readJson(_key);
    if (json == null) return null;
    return CalorieGoal.fromJson(json);
  }

  @override
  Future<void> save(CalorieGoal goal) async {
    await _cache.writeJson(_key, goal.toJson());
  }
}
