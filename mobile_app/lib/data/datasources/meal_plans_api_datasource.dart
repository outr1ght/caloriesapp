import '../../core/network/api_client.dart';

class MealPlansApiDatasource {
  MealPlansApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> list() async {
    final response = await _client.get<Map<String, dynamic>>('/meal-plans');
    return response.data ?? <String, dynamic>{};
  }
}
