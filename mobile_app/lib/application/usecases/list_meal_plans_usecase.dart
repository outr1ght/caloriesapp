import '../../domain/entities/meal_plan_entity.dart';
import '../../domain/repositories/meal_planner_repository.dart';

class ListMealPlansUseCase {
  const ListMealPlansUseCase(this._repository);

  final MealPlannerRepository _repository;

  Future<List<MealPlanEntity>> call() {
    return _repository.list();
  }
}
