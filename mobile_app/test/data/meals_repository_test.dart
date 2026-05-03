import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/api/generated/generated.dart';
import 'package:calories_mobile/data/datasources/meals_api_datasource.dart';
import 'package:calories_mobile/data/repositories/meal_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeMealsApiDatasource extends MealsApiDatasource {
  _FakeMealsApiDatasource() : super(DummyApiClient());

  @override
  Future<GeneratedMealListPage> list({int page = 1, int pageSize = 20}) async {
    return GeneratedMealListPage(
      items: [
        GeneratedMealRead(
          id: 'm1',
          userId: 'u1',
          title: 'Chicken bowl',
          notes: null,
          mealType: 'lunch',
          source: 'manual',
          eatenAt: DateTime.parse('2026-01-01T00:00:00Z').toUtc(),
          analysisStatus: 'ready',
          nutritionSummary: const GeneratedMealNutritionSummary(
            calories: 600,
            proteinG: 40,
            carbsG: 50,
            fatG: 20,
          ),
          items: const [],
          images: const [],
          createdAt: DateTime.utc(2026, 1, 1),
          updatedAt: DateTime.utc(2026, 1, 1),
        ),
      ],
      meta: const GeneratedPaginationMeta(page: 1, pageSize: 20, total: 1, totalPages: 1),
    );
  }
}

void main() {
  test('meal repository maps meal list from generated client dto', () async {
    final repo = MealRepositoryImpl(_FakeMealsApiDatasource());
    final items = await repo.list();
    expect(items.length, 1);
    expect(items.first.calories, 600);
    expect(items.first.mealType, 'lunch');
  });
}

