import '../entities/meal_plan_entity.dart';

abstract class MealPlannerRepository {
  Future<List<MealPlanEntity>> list();
}
