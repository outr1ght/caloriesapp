import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:calories_mobile/src/features/meals/application/meals_controller.dart';
import 'package:calories_mobile/src/features/meals/data/api_meals_repository.dart';
import 'package:calories_mobile/src/features/meals/domain/meal.dart';
import 'package:calories_mobile/src/features/meals/domain/meal_item.dart';
import 'package:calories_mobile/src/features/meals/domain/meals_repository.dart';

class _FakeMealsRepository implements MealsRepository {
  final List<Meal> _items = [];

  @override
  Future<Meal> createMeal({required String mealType, required List<MealItem> items, DateTime? consumedAt, String? imageId}) async {
    final meal = Meal(
      id: 'm1',
      mealType: mealType,
      items: items,
      nutrition: const NutritionTotals(calories: 500, proteinG: 40, fatG: 10, carbsG: 45),
      consumedAt: consumedAt ?? DateTime.now(),
    );
    _items.insert(0, meal);
    return meal;
  }

  @override
  Future<List<Meal>> listMeals({int page = 1, int pageSize = 20}) async {
    return _items;
  }
}

void main() {
  test('meals controller saveDemoMeal prepends meal', () async {
    final fake = _FakeMealsRepository();
    final container = ProviderContainer(overrides: [mealsRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(mealsControllerProvider.future);
    await container.read(mealsControllerProvider.notifier).saveDemoMeal();

    final state = container.read(mealsControllerProvider);
    expect(state.value?.length, 1);
  });
}
