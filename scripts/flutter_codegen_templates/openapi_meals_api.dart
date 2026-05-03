// GENERATED CODE - DO NOT MODIFY BY HAND.
// Source: docs/openapi/openapi.json

import '../../../core/network/api_client.dart';
import 'openapi_models.dart';

class GeneratedMealsApi {
  const GeneratedMealsApi(this._client);

  final ApiClient _client;

  Future<GeneratedMealListPage> listMeals({int page = 1, int pageSize = 20}) async {
    final response = await _client.get<Map<String, dynamic>>(
      '/meals',
      queryParameters: {'page': page, 'page_size': pageSize},
    );
    final root = response.data ?? const <String, dynamic>{};
    return GeneratedApiEnvelope.fromJson(root, (raw) {
      final data = (raw as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
      return GeneratedMealListPage.fromJson(data);
    }).data;
  }

  Future<GeneratedMealRead> getMeal(String id) async {
    final response = await _client.get<Map<String, dynamic>>('/meals/$id');
    final root = response.data ?? const <String, dynamic>{};
    return GeneratedApiEnvelope.fromJson(root, (raw) {
      final data = (raw as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
      return GeneratedMealRead.fromJson(data);
    }).data;
  }

  Future<GeneratedMealRead> updateMeal(String id, {String? title}) async {
    final response = await _client.patch<Map<String, dynamic>>('/meals/$id', data: {'title': title});
    final root = response.data ?? const <String, dynamic>{};
    return GeneratedApiEnvelope.fromJson(root, (raw) {
      final data = (raw as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
      return GeneratedMealRead.fromJson(data);
    }).data;
  }

  Future<void> deleteMeal(String id) async {
    await _client.delete<Map<String, dynamic>>('/meals/$id');
  }
}
