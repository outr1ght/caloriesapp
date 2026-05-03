// GENERATED CODE - DO NOT MODIFY BY HAND.
// Source: docs/openapi/openapi.json

import '../../../core/network/api_client.dart';
import 'openapi_models.dart';

class GeneratedAuthApi {
  const GeneratedAuthApi(this._client);

  final ApiClient _client;

  Future<GeneratedAuthSession> login(GeneratedLoginRequest request) async {
    final response = await _client.post<Map<String, dynamic>>('/auth/login', data: request.toJson());
    final root = response.data ?? const <String, dynamic>{};
    return GeneratedApiEnvelope.fromJson(root, (raw) {
      final data = (raw as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
      return GeneratedAuthSession.fromJson(data);
    }).data;
  }

  Future<GeneratedAuthSession> register(GeneratedRegisterRequest request) async {
    final response = await _client.post<Map<String, dynamic>>('/auth/register', data: request.toJson());
    final root = response.data ?? const <String, dynamic>{};
    return GeneratedApiEnvelope.fromJson(root, (raw) {
      final data = (raw as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
      return GeneratedAuthSession.fromJson(data);
    }).data;
  }

  Future<void> logout(GeneratedLogoutRequest request) async {
    await _client.post<Map<String, dynamic>>('/auth/logout', data: request.toJson());
  }
}
