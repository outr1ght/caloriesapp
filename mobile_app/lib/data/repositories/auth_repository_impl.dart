import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client.dart';
import '../../core/network/api_client_provider.dart';
import '../../core/storage/token_storage.dart';
import '../../domain/entities/user_session.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_api_datasource.dart';

final authApiDatasourceProvider = Provider<AuthApiDatasource>((ref) {
  return AuthApiDatasource(ref.read(apiClientProvider));
});

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepositoryImpl(
    datasource: ref.read(authApiDatasourceProvider),
    tokenStorage: ref.read(tokenStorageProvider),
    apiClient: ref.read(apiClientProvider),
  );
});

class AuthRepositoryImpl implements AuthRepository {
  AuthRepositoryImpl({required this.datasource, required this.tokenStorage, required this.apiClient});

  final AuthApiDatasource datasource;
  final TokenStorage tokenStorage;
  final ApiClient apiClient;

  @override
  Future<UserSession> login(String email, String password) async {
    final tokens = await datasource.login(email, password);
    final session = UserSession(accessToken: tokens.accessToken, refreshToken: tokens.refreshToken);
    await apiClient.applySession(session);
    return session;
  }

  @override
  Future<UserSession> signup(String email, String password) async {
    final tokens = await datasource.signup(email, password);
    final session = UserSession(accessToken: tokens.accessToken, refreshToken: tokens.refreshToken);
    await apiClient.applySession(session);
    return session;
  }

  @override
  Future<UserSession?> restoreSession() async {
    final session = await tokenStorage.read();
    await apiClient.applySession(session);
    return session;
  }

  @override
  Future<void> logout() async {
    final session = await tokenStorage.read();
    try {
      await datasource.logout(session?.refreshToken);
    } catch (_) {
      // ignore logout network failures and clear local session
    }
    await apiClient.applySession(null);
  }
}
