import '../../core/network/api_client.dart';
import '../models/auth_models.dart';

class AuthApiDatasource {
  AuthApiDatasource(this._apiClient);

  final ApiClient _apiClient;

  Future<AuthTokensModel> login(String email, String password) async {
    final response = await _apiClient.post<Map<String, dynamic>>(
      '/auth/login',
      data: {'email': email, 'password': password},
    );

    final root = response.data ?? <String, dynamic>{};
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return AuthTokensModel.fromApi(data);
  }

  Future<AuthTokensModel> signup(String email, String password) async {
    final registerResponse = await _apiClient.post<Map<String, dynamic>>(
      '/auth/register',
      data: {'email': email, 'password': password},
    );

    final regRoot = registerResponse.data ?? <String, dynamic>{};
    final regData = (regRoot['data'] as Map<String, dynamic>?) ?? regRoot;
    final tokens = AuthTokensModel.fromApi(regData);

    if (tokens.accessToken.isNotEmpty && tokens.refreshToken.isNotEmpty) {
      return tokens;
    }

    return login(email, password);
  }

  Future<void> logout(String? refreshToken) async {
    if (refreshToken == null || refreshToken.isEmpty) return;
    await _apiClient.post<Map<String, dynamic>>('/auth/logout', data: {'refresh_token': refreshToken});
  }
}
