import '../domain/meals_repository.dart';
import '../domain/meal.dart';
import '../domain/meal_item.dart';

class AnalyzeMealUseCase {
  const AnalyzeMealUseCase(this._repository);

  final MealsRepository _repository;

  Future<Meal> createDemoMeal() {
    return _repository.createMeal(
      mealType: 'lunch',
      items: const [
        MealItem(name: 'chicken breast', grams: 160, confidence: 0.81),
        MealItem(name: 'rice', grams: 120, confidence: 0.73),
        MealItem(name: 'broccoli', grams: 80, confidence: 0.68),
      ],
      consumedAt: DateTime.now().toUtc(),
    );
  }
}
