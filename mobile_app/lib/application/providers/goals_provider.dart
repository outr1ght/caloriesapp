import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/goals_repository_impl.dart';
import '../../domain/entities/goal_entity.dart';
import '../usecases/get_goal_usecase.dart';
import '../usecases/save_goal_usecase.dart';

final goalsProvider = AsyncNotifierProvider<GoalsController, GoalEntity?>(GoalsController.new);

class GoalsController extends AsyncNotifier<GoalEntity?> {
  @override
  Future<GoalEntity?> build() async {
    final usecase = GetGoalUseCase(ref.read(goalsRepositoryProvider));
    return usecase();
  }

  Future<void> save(GoalEntity goal) async {
    final usecase = SaveGoalUseCase(ref.read(goalsRepositoryProvider));
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => usecase(goal));
  }

  Future<bool> isCompleted() {
    return ref.read(goalsRepositoryProvider).hasActiveGoal();
  }
}
