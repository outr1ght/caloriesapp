import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/api_meals_repository.dart';
import '../domain/meal.dart';
import '../domain/meal_item.dart';

final mealsControllerProvider = AsyncNotifierProvider<MealsController, List<Meal>>(MealsController.new);

class MealsController extends AsyncNotifier<List<Meal>> {
  @override
  Future<List<Meal>> build() async {
    return ref.read(mealsRepositoryProvider).listMeals();
  }

  Future<void> refreshMeals() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => ref.read(mealsRepositoryProvider).listMeals());
  }

  Future<void> saveDemoMeal() async {
    final repo = ref.read(mealsRepositoryProvider);
    final meal = await repo.createMeal(
      mealType: 'lunch',
      items: const [
        MealItem(name: 'chicken breast', grams: 160, confidence: 0.81),
        MealItem(name: 'rice', grams: 120, confidence: 0.73),
        MealItem(name: 'broccoli', grams: 80, confidence: 0.68),
      ],
      consumedAt: DateTime.now().toUtc(),
    );

    final current = state.valueOrNull ?? <Meal>[];
    state = AsyncData([meal, ...current]);
  }
}
