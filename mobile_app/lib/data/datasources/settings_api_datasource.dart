import '../../core/network/api_client.dart';

class SettingsApiDatasource {
  SettingsApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> getSettings() async {
    final response = await _client.get<Map<String, dynamic>>('/settings');
    return response.data ?? <String, dynamic>{};
  }

  Future<Map<String, dynamic>> patchSettings(Map<String, dynamic> payload) async {
    final response = await _client.patch<Map<String, dynamic>>('/settings', data: payload);
    return response.data ?? <String, dynamic>{};
  }
}
