import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/goals_api_datasource.dart';
import 'package:calories_mobile/data/repositories/goals_repository_impl.dart';
import 'package:calories_mobile/domain/entities/goal_entity.dart';

import '../helpers/test_helpers.dart';

class _FakeGoalsApiDatasource extends GoalsApiDatasource {
  _FakeGoalsApiDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> getActive() async => {
    'data': {
      'id': 'g1',
      'activity_level': 'moderate',
      'strategy': 'maintain',
      'target_calories': '2200',
      'target_protein_g': '120',
      'target_carbs_g': '200',
      'target_fat_g': '70'
    }
  };

  @override
  Future<Map<String, dynamic>> update(String goalId, Map<String, dynamic> payload) async => {
    'data': {
      'id': goalId,
      ...payload,
    }
  };
}

void main() {
  test('goals repository returns active goal', () async {
    final repo = GoalsRepositoryImpl(_FakeGoalsApiDatasource());
    final goal = await repo.getActiveGoal();
    expect(goal?.id, 'g1');
  });

  test('goals repository updates active goal', () async {
    final repo = GoalsRepositoryImpl(_FakeGoalsApiDatasource());
    final saved = await repo.saveGoal(const GoalEntity(
      id: '',
      activityLevel: 'moderate',
      strategy: 'maintain',
      targetCalories: 2300,
      targetProtein: 130,
      targetCarbs: 210,
      targetFat: 75,
    ));
    expect(saved.targetCalories, 2300);
  });
}
