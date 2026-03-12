import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/meal_planner_repository_impl.dart';
import '../../domain/entities/meal_plan_entity.dart';
import '../usecases/list_meal_plans_usecase.dart';

final mealPlannerProvider = AsyncNotifierProvider<MealPlannerController, List<MealPlanEntity>>(
  MealPlannerController.new,
);

class MealPlannerController extends AsyncNotifier<List<MealPlanEntity>> {
  @override
  Future<List<MealPlanEntity>> build() async {
    final usecase = ListMealPlansUseCase(ref.read(mealPlannerRepositoryProvider));
    return usecase();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = ListMealPlansUseCase(ref.read(mealPlannerRepositoryProvider));
      return usecase();
    });
  }
}
