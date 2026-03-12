import '../../core/network/api_client.dart';

class MealsApiDatasource {
  MealsApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> list({int page = 1, int pageSize = 20}) async {
    final response = await _client.get<Map<String, dynamic>>(
      '/meals',
      queryParameters: {'page': page, 'page_size': pageSize},
    );
    return response.data ?? <String, dynamic>{};
  }

  Future<Map<String, dynamic>> getById(String id) async {
    final response = await _client.get<Map<String, dynamic>>('/meals/$id');
    return response.data ?? <String, dynamic>{};
  }
}
