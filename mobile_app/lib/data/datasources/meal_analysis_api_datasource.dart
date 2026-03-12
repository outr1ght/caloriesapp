import '../../core/network/api_client.dart';

class MealAnalysisApiDatasource {
  MealAnalysisApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> analyze({required String uploadedImageId, String? mealId}) async {
    final response = await _client.post<Map<String, dynamic>>(
      '/meals/analysis',
      data: {
        'meal_id': mealId,
        'uploaded_image_ids': [uploadedImageId],
      },
    );

    return response.data ?? <String, dynamic>{};
  }

  Future<Map<String, dynamic>> createMeal(Map<String, dynamic> payload) async {
    final response = await _client.post<Map<String, dynamic>>('/meals', data: payload);
    return response.data ?? <String, dynamic>{};
  }
}
