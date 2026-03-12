import '../../core/network/api_client.dart';

class WeightsApiDatasource {
  WeightsApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> list({int page = 1, int pageSize = 30}) async {
    final response = await _client.get<Map<String, dynamic>>(
      '/weights',
      queryParameters: {'page': page, 'page_size': pageSize},
    );
    return response.data ?? <String, dynamic>{};
  }

  Future<Map<String, dynamic>> create({required double weightKg, required DateTime loggedAt}) async {
    final response = await _client.post<Map<String, dynamic>>(
      '/weights',
      data: {
        'logged_at': loggedAt.toUtc().toIso8601String(),
        'weight_kg': weightKg,
      },
    );
    return response.data ?? <String, dynamic>{};
  }
}
