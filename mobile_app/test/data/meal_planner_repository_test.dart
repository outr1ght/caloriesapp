import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/meal_plans_api_datasource.dart';
import 'package:calories_mobile/data/repositories/meal_planner_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeMealPlansDatasource extends MealPlansApiDatasource {
  _FakeMealPlansDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> list() async => {
    'data': {
      'items': [
        {'id': 'p1', 'title': 'Week plan', 'status': 'active', 'plan_date': '2026-01-01'}
      ]
    }
  };
}

void main() {
  test('meal planner repository maps plans', () async {
    final repo = MealPlannerRepositoryImpl(_FakeMealPlansDatasource());
    final plans = await repo.list();
    expect(plans.first.title, 'Week plan');
  });
}
