import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/goals_provider.dart';
import 'package:calories_mobile/data/repositories/goals_repository_impl.dart';
import 'package:calories_mobile/domain/entities/goal_entity.dart';
import 'package:calories_mobile/domain/repositories/goals_repository.dart';

class _FakeGoalsRepository implements GoalsRepository {
  GoalEntity? _goal;

  @override
  Future<GoalEntity?> getActiveGoal() async => _goal;

  @override
  Future<bool> hasActiveGoal() async => _goal != null;

  @override
  Future<GoalEntity> saveGoal(GoalEntity goal) async {
    _goal = goal;
    return goal;
  }
}

void main() {
  test('goals provider save updates state', () async {
    final fake = _FakeGoalsRepository();
    final container = ProviderContainer(overrides: [goalsRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(goalsProvider.future);
    await container.read(goalsProvider.notifier).save(const GoalEntity(
      id: 'g1',
      activityLevel: 'moderate',
      strategy: 'maintain',
      targetCalories: 2200,
      targetProtein: 120,
      targetCarbs: 200,
      targetFat: 70,
    ));

    expect(container.read(goalsProvider).valueOrNull?.targetCalories, 2200);
  });
}
