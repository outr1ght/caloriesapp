import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../domain/entities/user_session.dart';

final secureStorageProvider = Provider<FlutterSecureStorage>((_) => const FlutterSecureStorage());

final tokenStorageProvider = Provider<TokenStorage>((ref) {
  return TokenStorage(ref.read(secureStorageProvider));
});

class TokenStorage {
  TokenStorage(this._storage);

  final FlutterSecureStorage _storage;
  static const _key = 'auth_session_v1';

  Future<void> save(UserSession session) async {
    await _storage.write(key: _key, value: jsonEncode(session.toJson()));
  }

  Future<UserSession?> read() async {
    final raw = await _storage.read(key: _key);
    if (raw == null || raw.isEmpty) return null;

    final decoded = jsonDecode(raw);
    if (decoded is! Map<String, dynamic>) return null;
    return UserSession.fromJson(decoded);
  }

  Future<void> clear() => _storage.delete(key: _key);
}
