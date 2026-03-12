import '../entities/meal_analysis_entity.dart';

abstract class MealAnalysisRepository {
  Future<MealAnalysisEntity> analyze(String uploadedImageId, {String? mealId});
  Future<String> saveMealFromAnalysis(MealAnalysisEntity analysis, {String mealType = 'lunch'});
}
