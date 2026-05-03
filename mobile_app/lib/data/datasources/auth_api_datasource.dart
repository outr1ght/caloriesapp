import '../../core/network/api_client.dart';
import '../api/generated/generated.dart';
import '../models/auth_models.dart';

class AuthApiDatasource {
  AuthApiDatasource(this._apiClient) : _generated = GeneratedAuthApi(_apiClient);

  final ApiClient _apiClient;
  final GeneratedAuthApi _generated;

  Future<AuthTokensModel> login(String email, String password) async {
    final session = await _generated.login(GeneratedLoginRequest(email: email, password: password));
    return AuthTokensModel.fromGenerated(session);
  }

  Future<AuthTokensModel> signup(String email, String password) async {
    final session = await _generated.register(GeneratedRegisterRequest(email: email, password: password));
    final tokens = AuthTokensModel.fromGenerated(session);

    if (tokens.accessToken.isNotEmpty && tokens.refreshToken.isNotEmpty) {
      return tokens;
    }

    return login(email, password);
  }

  Future<Map<String, dynamic>> getCurrentUser() async {
    final response = await _apiClient.get<Map<String, dynamic>>('/me');
    return response.data ?? <String, dynamic>{};
  }

  Future<void> logout(String? refreshToken) async {
    if (refreshToken == null || refreshToken.isEmpty) return;
    await _generated.logout(GeneratedLogoutRequest(refreshToken: refreshToken));
  }
}
