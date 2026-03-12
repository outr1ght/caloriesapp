import '../../core/network/api_client.dart';

class ReportsApiDatasource {
  ReportsApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> fetchNutrition({
    required DateTime from,
    required DateTime to,
  }) async {
    final response = await _client.get<Map<String, dynamic>>(
      '/reports/nutrition',
      queryParameters: {
        'date_from': _formatDate(from),
        'date_to': _formatDate(to),
      },
    );

    return response.data ?? <String, dynamic>{};
  }

  String _formatDate(DateTime dt) {
    final y = dt.year.toString().padLeft(4, '0');
    final m = dt.month.toString().padLeft(2, '0');
    final d = dt.day.toString().padLeft(2, '0');
    return '$y-$m-$d';
  }
}
