import '../../core/network/api_client.dart';

class RecommendationsApiDatasource {
  RecommendationsApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> list({String? status, int page = 1, int pageSize = 20}) async {
    final query = <String, dynamic>{'page': page, 'page_size': pageSize};
    if (status != null && status.isNotEmpty) {
      query['status'] = status;
    }

    final response = await _client.get<Map<String, dynamic>>('/recommendations', queryParameters: query);
    return response.data ?? <String, dynamic>{};
  }

  Future<void> updateStatus(String id, String status) async {
    await _client.patch<Map<String, dynamic>>('/recommendations/$id/status', data: {'status': status});
  }
}
