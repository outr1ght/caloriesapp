import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/meal_repository_impl.dart';
import '../../domain/entities/meal_entity.dart';
import '../usecases/get_meal_by_id_usecase.dart';

final mealDetailProvider = FutureProvider.family<MealEntity, String>((ref, mealId) async {
  final usecase = GetMealByIdUseCase(ref.read(mealRepositoryProvider));
  return usecase(mealId);
});
