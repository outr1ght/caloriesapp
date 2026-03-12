import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/auth_api_datasource.dart';
import 'package:calories_mobile/data/repositories/auth_repository_impl.dart';

import 'package:calories_mobile/domain/entities/user_session.dart';

import '../helpers/test_helpers.dart';

void main() {
  test('auth repository login returns session tokens', () async {
    final api = DummyApiClient();
    api.postResponses['/auth/login'] = {
      'data': {
        'tokens': {'access_token': 'a1', 'refresh_token': 'r1'}
      }
    };

    final datasource = AuthApiDatasource(api);
    final tokenStorage = InMemoryTokenStorage();
    final repo = AuthRepositoryImpl(datasource: datasource, tokenStorage: tokenStorage, apiClient: api);

    final session = await repo.login('u@example.com', 'secret');
    expect(session.accessToken, 'a1');
    expect(session.refreshToken, 'r1');
  });

  test('auth repository restore session reads storage', () async {
    final api = DummyApiClient();
    final datasource = AuthApiDatasource(api);
    final tokenStorage = InMemoryTokenStorage();
    await tokenStorage.save(const UserSession(accessToken: 'a2', refreshToken: 'r2'));

    final repo = AuthRepositoryImpl(datasource: datasource, tokenStorage: tokenStorage, apiClient: api);
    final restored = await repo.restoreSession();

    expect(restored?.accessToken, 'a2');
  });
}
