import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:calories_mobile/src/features/auth/application/auth_controller.dart';
import 'package:calories_mobile/src/features/auth/data/api_auth_repository.dart';
import 'package:calories_mobile/src/features/auth/domain/auth_repository.dart';
import 'package:calories_mobile/src/features/auth/domain/auth_session.dart';

class _FakeAuthRepository implements AuthRepository {
  AuthSession? _session;

  @override
  Future<AuthSession> login(String email, String password) async {
    _session = const AuthSession(accessToken: 'a', refreshToken: 'r');
    return _session!;
  }

  @override
  Future<void> logout() async {
    _session = null;
  }

  @override
  Future<AuthSession?> restoreSession() async {
    return _session;
  }
}

void main() {
  test('auth controller login updates state', () async {
    final fake = _FakeAuthRepository();
    final container = ProviderContainer(overrides: [authRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(authControllerProvider.future);
    await container.read(authControllerProvider.notifier).login('u@example.com', 'secret');

    final state = container.read(authControllerProvider);
    expect(state.hasValue, isTrue);
    expect(state.value?.accessToken, 'a');
  });
}
