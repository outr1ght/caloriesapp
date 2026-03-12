import '../../core/network/api_client.dart';

class BarcodeApiDatasource {
  BarcodeApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> lookup(String code) async {
    final response = await _client.post<Map<String, dynamic>>('/barcodes/lookup', data: {'code': code});
    return response.data ?? <String, dynamic>{};
  }

  Future<Map<String, dynamic>> saveAsMeal(String name) async {
    final response = await _client.post<Map<String, dynamic>>(
      '/meals',
      data: {
        'title': name,
        'meal_type': 'snack',
        'source': 'barcode',
        'eaten_at': DateTime.now().toUtc().toIso8601String(),
        'items': [
          {'display_name': name, 'quantity': 1, 'unit': 'serving', 'position': 0}
        ],
      },
    );
    return response.data ?? <String, dynamic>{};
  }
}
