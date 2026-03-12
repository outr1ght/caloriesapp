import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/profile_api_datasource.dart';
import 'package:calories_mobile/data/repositories/profile_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeProfileApiDatasource extends ProfileApiDatasource {
  _FakeProfileApiDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> getMe() async => {
    'data': {
      'profile': {
        'first_name': 'John',
        'last_name': 'Doe',
        'birth_year': 1990,
        'gender': 'male',
        'height_cm': 180,
      }
    }
  };

  @override
  Future<Map<String, dynamic>> listWeights() async => {
    'data': {
      'items': [
        {'id': 'w1', 'logged_at': '2026-01-01T00:00:00Z', 'weight_kg': '80.0'}
      ]
    }
  };

  @override
  Future<String> getActivityLevel() async => 'moderate';
}

void main() {
  test('profile repository maps me + weights', () async {
    final repo = ProfileRepositoryImpl(_FakeProfileApiDatasource());
    final profile = await repo.getProfile();

    expect(profile, isNotNull);
    expect(profile!.firstName, 'John');
    expect(profile.weightKg, 80.0);
  });
}
