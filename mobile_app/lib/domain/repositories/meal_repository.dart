import '../entities/meal_entity.dart';

abstract class MealRepository {
  Future<List<MealEntity>> list({int page = 1, int pageSize = 20});
  Future<MealEntity> getById(String id);
}
