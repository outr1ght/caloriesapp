import '../../domain/entities/meal_analysis_entity.dart';
import '../../domain/repositories/meal_analysis_repository.dart';

class SaveMealFromAnalysisUseCase {
  const SaveMealFromAnalysisUseCase(this._repository);

  final MealAnalysisRepository _repository;

  Future<String> call(MealAnalysisEntity analysis, {String mealType = 'lunch'}) {
    return _repository.saveMealFromAnalysis(analysis, mealType: mealType);
  }
}
