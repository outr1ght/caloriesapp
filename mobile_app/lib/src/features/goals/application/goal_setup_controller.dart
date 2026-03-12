import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/local_calorie_goal_repository.dart';
import '../domain/calorie_goal.dart';

final goalSetupControllerProvider = AsyncNotifierProvider<GoalSetupController, CalorieGoal?>(GoalSetupController.new);

class GoalSetupController extends AsyncNotifier<CalorieGoal?> {
  @override
  Future<CalorieGoal?> build() async {
    return ref.read(calorieGoalRepositoryProvider).load();
  }

  Future<void> save(CalorieGoal goal) async {
    await ref.read(calorieGoalRepositoryProvider).save(goal);
    state = AsyncData(goal);
  }
}
