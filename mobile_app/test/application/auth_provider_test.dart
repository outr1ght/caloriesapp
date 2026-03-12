import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/auth_provider.dart';
import 'package:calories_mobile/data/repositories/auth_repository_impl.dart';
import 'package:calories_mobile/domain/entities/user_session.dart';
import 'package:calories_mobile/domain/repositories/auth_repository.dart';

class _FakeAuthRepository implements AuthRepository {
  UserSession? _session;

  @override
  Future<UserSession> login(String email, String password) async {
    _session = const UserSession(accessToken: 'token', refreshToken: 'refresh');
    return _session!;
  }

  @override
  Future<void> logout() async {
    _session = null;
  }

  @override
  Future<UserSession?> restoreSession() async {
    return _session;
  }

  @override
  Future<UserSession> signup(String email, String password) async {
    _session = const UserSession(accessToken: 'token2', refreshToken: 'refresh2');
    return _session!;
  }
}

void main() {
  test('auth provider login updates session', () async {
    final fake = _FakeAuthRepository();
    final container = ProviderContainer(overrides: [authRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(authStateProvider.future);
    await container.read(authStateProvider.notifier).login('u@example.com', 'secret');

    final state = container.read(authStateProvider);
    expect(state.valueOrNull?.accessToken, 'token');
  });
}
