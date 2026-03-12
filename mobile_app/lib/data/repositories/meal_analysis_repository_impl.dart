import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/meal_analysis_entity.dart';
import '../../domain/repositories/meal_analysis_repository.dart';
import '../datasources/meal_analysis_api_datasource.dart';
import '../models/meal_analysis_models.dart';

final mealAnalysisApiDatasourceProvider = Provider<MealAnalysisApiDatasource>((ref) {
  return MealAnalysisApiDatasource(ref.read(apiClientProvider));
});

final mealAnalysisRepositoryProvider = Provider<MealAnalysisRepository>((ref) {
  return MealAnalysisRepositoryImpl(ref.read(mealAnalysisApiDatasourceProvider));
});

class MealAnalysisRepositoryImpl implements MealAnalysisRepository {
  MealAnalysisRepositoryImpl(this._datasource);

  final MealAnalysisApiDatasource _datasource;

  @override
  Future<MealAnalysisEntity> analyze(String uploadedImageId, {String? mealId}) async {
    final root = await _datasource.analyze(uploadedImageId: uploadedImageId, mealId: mealId);
    return MealAnalysisModel.fromApi(root).toEntity();
  }

  @override
  Future<String> saveMealFromAnalysis(MealAnalysisEntity analysis, {String mealType = 'lunch'}) async {
    final payload = {
      'title': analysis.items.isNotEmpty ? analysis.items.first.name : 'Analyzed meal',
      'meal_type': mealType,
      'source': 'image_analysis',
      'eaten_at': DateTime.now().toUtc().toIso8601String(),
      'items': analysis.items
          .map(
            (item) => {
              'display_name': item.name,
              'quantity': item.quantity,
              'unit': item.unit,
              'position': 0,
            },
          )
          .toList(),
    };

    final root = await _datasource.createMeal(payload);
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return (data['id'] as String?) ?? '';
  }
}
