import 'meal.dart';
import 'meal_item.dart';

abstract class MealsRepository {
  Future<List<Meal>> listMeals({int page = 1, int pageSize = 20});
  Future<Meal> createMeal({required String mealType, required List<MealItem> items, DateTime? consumedAt, String? imageId});
}
