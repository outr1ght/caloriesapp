class AuthTokensModel {
  const AuthTokensModel({required this.accessToken, required this.refreshToken});

  final String accessToken;
  final String refreshToken;

  factory AuthTokensModel.fromApi(Map<String, dynamic> data) {
    final tokens = (data['tokens'] as Map<String, dynamic>?) ?? data;
    return AuthTokensModel(
      accessToken: (tokens['access_token'] as String?) ?? '',
      refreshToken: (tokens['refresh_token'] as String?) ?? '',
    );
  }
}
