import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/api_client.dart';
import '../../../core/network/dio_client.dart';
import '../../../core/storage/session_storage.dart';
import '../domain/auth_repository.dart';
import '../domain/auth_session.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return ApiAuthRepository(
    ref.read(apiClientProvider),
    ref.read(sessionStorageProvider),
  );
});

class ApiAuthRepository implements AuthRepository {
  ApiAuthRepository(this._apiClient, this._sessionStorage);

  final ApiClient _apiClient;
  final SessionStorage _sessionStorage;

  @override
  Future<AuthSession> login(String email, String password) async {
    final response = await _apiClient.post<Map<String, dynamic>>(
      '/auth/login',
      data: {'email': email, 'password': password},
    );

    final data = response.data ?? <String, dynamic>{};
    final access = data['access_token'] as String?;
    final refresh = data['refresh_token'] as String?;
    if (access == null || refresh == null) {
      throw StateError('Invalid login response');
    }

    final session = AuthSession(accessToken: access, refreshToken: refresh);
    await _apiClient.setSession(session);
    return session;
  }

  @override
  Future<AuthSession?> restoreSession() async {
    final session = await _sessionStorage.read();
    await _apiClient.setSession(session);
    return session;
  }

  @override
  Future<void> logout() async {
    await _apiClient.setSession(null);
  }
}
