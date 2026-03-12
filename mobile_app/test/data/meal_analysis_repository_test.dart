import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/meal_analysis_api_datasource.dart';
import 'package:calories_mobile/data/repositories/meal_analysis_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeMealAnalysisDatasource extends MealAnalysisApiDatasource {
  _FakeMealAnalysisDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> analyze({required String uploadedImageId, String? mealId}) async => {
    'data': {
      'meal_id': 'm1',
      'status': 'ready',
      'items': [
        {'name': 'Rice', 'estimated_quantity': 150, 'unit': 'g', 'confidence': 0.8}
      ],
      'estimated_nutrition': {
        'calories': 250,
        'protein_g': 5,
        'carbs_g': 50,
        'fat_g': 1,
        'confidence': 0.8
      },
      'explanation': 'ok',
      'warnings': []
    }
  };

  @override
  Future<Map<String, dynamic>> createMeal(Map<String, dynamic> payload) async => {
    'data': {'id': 'meal-created'}
  };
}

void main() {
  test('meal analysis repository analyze maps response', () async {
    final repo = MealAnalysisRepositoryImpl(_FakeMealAnalysisDatasource());
    final result = await repo.analyze('img1');
    expect(result.items.first.name, 'Rice');
    expect(result.calories, 250);
  });
}
