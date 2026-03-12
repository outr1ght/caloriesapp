class UserSession {
  const UserSession({required this.accessToken, required this.refreshToken});

  final String accessToken;
  final String refreshToken;

  Map<String, dynamic> toJson() => {
        'access_token': accessToken,
        'refresh_token': refreshToken,
      };

  factory UserSession.fromJson(Map<String, dynamic> json) {
    return UserSession(
      accessToken: (json['access_token'] as String?) ?? '',
      refreshToken: (json['refresh_token'] as String?) ?? '',
    );
  }
}
