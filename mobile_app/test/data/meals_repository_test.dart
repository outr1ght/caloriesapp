import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/meals_api_datasource.dart';
import 'package:calories_mobile/data/repositories/meal_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeMealsApiDatasource extends MealsApiDatasource {
  _FakeMealsApiDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> list({int page = 1, int pageSize = 20}) async => {
    'data': {
      'items': [
        {
          'id': 'm1',
          'meal_type': 'lunch',
          'logged_at': '2026-01-01T00:00:00Z',
          'nutrition': {'calories': 600}
        }
      ]
    }
  };
}

void main() {
  test('meal repository maps meal list', () async {
    final repo = MealRepositoryImpl(_FakeMealsApiDatasource());
    final items = await repo.list();
    expect(items.length, 1);
    expect(items.first.calories, 600);
  });
}
