import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/meal_repository_impl.dart';
import '../../domain/entities/meal_entity.dart';
import '../usecases/list_meals_usecase.dart';

final mealsProvider = AsyncNotifierProvider<MealsController, List<MealEntity>>(MealsController.new);

class MealsController extends AsyncNotifier<List<MealEntity>> {
  @override
  Future<List<MealEntity>> build() async {
    final usecase = ListMealsUseCase(ref.read(mealRepositoryProvider));
    return usecase();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = ListMealsUseCase(ref.read(mealRepositoryProvider));
      return usecase();
    });
  }
}
