import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/api_client.dart';
import '../../../core/network/dio_client.dart';
import '../domain/meal.dart';
import '../domain/meal_item.dart';
import '../domain/meals_repository.dart';

final mealsRepositoryProvider = Provider<MealsRepository>((ref) {
  return ApiMealsRepository(ref.read(apiClientProvider));
});

class ApiMealsRepository implements MealsRepository {
  ApiMealsRepository(this._apiClient);

  final ApiClient _apiClient;

  @override
  Future<List<Meal>> listMeals({int page = 1, int pageSize = 20}) async {
    final response = await _apiClient.get<Map<String, dynamic>>(
      '/meals',
      queryParameters: {'page': page, 'page_size': pageSize},
    );

    final root = response.data ?? <String, dynamic>{};
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    final items = (data['items'] as List<dynamic>? ?? <dynamic>[])
        .whereType<Map<String, dynamic>>()
        .map(_mealFromJson)
        .toList();
    return items;
  }

  @override
  Future<Meal> createMeal({required String mealType, required List<MealItem> items, DateTime? consumedAt, String? imageId}) async {
    final response = await _apiClient.post<Map<String, dynamic>>(
      '/meals',
      data: {
        'meal_type': mealType,
        'source': imageId != null ? 'image_analysis' : 'manual',
        'eaten_at': (consumedAt ?? DateTime.now().toUtc()).toIso8601String(),
        'items': items
            .map((e) => {'display_name': e.name, 'quantity': e.grams, 'unit': 'g'})
            .toList(),
      },
    );

    final root = response.data ?? <String, dynamic>{};
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return _mealFromJson(data);
  }

  Meal _mealFromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List<dynamic>? ?? <dynamic>[])
        .whereType<Map<String, dynamic>>()
        .map(
          (e) => MealItem(
            name: (e['display_name'] as String?) ?? (e['name'] as String?) ?? '',
            grams: ((e['quantity'] as num?) ?? (e['grams'] as num?) ?? 0).toDouble(),
            confidence: ((e['confidence'] as num?) ?? 1).toDouble(),
          ),
        )
        .toList();

    final nutrition = (json['nutrition_value'] as Map<String, dynamic>?) ??
        (json['nutrition'] as Map<String, dynamic>?) ??
        <String, dynamic>{};

    return Meal(
      id: (json['id'] as String?) ?? (json['meal_id'] as String?) ?? '',
      mealType: (json['meal_type'] as String?) ?? 'lunch',
      items: items,
      nutrition: NutritionTotals(
        calories: ((nutrition['calories'] as num?) ?? 0).toDouble(),
        proteinG: ((nutrition['protein_g'] as num?) ?? 0).toDouble(),
        fatG: ((nutrition['fat_g'] as num?) ?? 0).toDouble(),
        carbsG: ((nutrition['carbs_g'] as num?) ?? 0).toDouble(),
      ),
      consumedAt: DateTime.tryParse((json['eaten_at'] as String?) ?? (json['consumed_at'] as String?) ?? '') ?? DateTime.now(),
    );
  }
}
