import '../../core/network/api_client.dart';

class GoalsApiDatasource {
  GoalsApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> getActive() async {
    final response = await _client.get<Map<String, dynamic>>('/goals/active');
    return response.data ?? <String, dynamic>{};
  }

  Future<Map<String, dynamic>> create(Map<String, dynamic> payload) async {
    final response = await _client.post<Map<String, dynamic>>('/goals', data: payload);
    return response.data ?? <String, dynamic>{};
  }

  Future<Map<String, dynamic>> update(String goalId, Map<String, dynamic> payload) async {
    final response = await _client.patch<Map<String, dynamic>>('/goals/$goalId', data: payload);
    return response.data ?? <String, dynamic>{};
  }
}
