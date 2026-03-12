import 'dart:convert';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../features/auth/domain/auth_session.dart';

class SessionStorage {
  SessionStorage(this._secureStorage);

  final FlutterSecureStorage _secureStorage;

  static const _sessionKey = 'auth_session_v1';

  Future<void> save(AuthSession session) async {
    final payload = jsonEncode({'access_token': session.accessToken, 'refresh_token': session.refreshToken});
    await _secureStorage.write(key: _sessionKey, value: payload);
  }

  Future<AuthSession?> read() async {
    final raw = await _secureStorage.read(key: _sessionKey);
    if (raw == null || raw.isEmpty) return null;
    final parsed = jsonDecode(raw) as Map<String, dynamic>;
    final access = parsed['access_token'] as String?;
    final refresh = parsed['refresh_token'] as String?;
    if (access == null || refresh == null) return null;
    return AuthSession(accessToken: access, refreshToken: refresh);
  }

  Future<void> clear() async {
    await _secureStorage.delete(key: _sessionKey);
  }
}
