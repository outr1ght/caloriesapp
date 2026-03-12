import '../../domain/entities/meal_analysis_entity.dart';
import '../../domain/repositories/meal_analysis_repository.dart';

class AnalyzeMealUseCase {
  const AnalyzeMealUseCase(this._repository);

  final MealAnalysisRepository _repository;

  Future<MealAnalysisEntity> call(String uploadedImageId, {String? mealId}) {
    return _repository.analyze(uploadedImageId, mealId: mealId);
  }
}
