import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/settings_api_datasource.dart';
import 'package:calories_mobile/data/repositories/settings_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeSettingsDatasource extends SettingsApiDatasource {
  _FakeSettingsDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> getSettings() async => {
    'data': {
      'id': 's1',
      'user_id': 'u1',
      'language': 'en',
      'unit_system': 'metric',
      'notifications_enabled': true,
      'meal_reminder_enabled': false
    }
  };

  @override
  Future<Map<String, dynamic>> patchSettings(Map<String, dynamic> payload) async => {
    'data': {
      'id': 's1',
      'user_id': 'u1',
      'language': payload['language'] ?? 'en',
      'unit_system': payload['unit_system'] ?? 'metric',
      'notifications_enabled': payload['notifications_enabled'] ?? true,
      'meal_reminder_enabled': payload['meal_reminder_enabled'] ?? false,
    }
  };
}

void main() {
  test('settings repository maps settings', () async {
    final repo = SettingsRepositoryImpl(_FakeSettingsDatasource());
    final settings = await repo.getSettings();
    expect(settings.language, 'en');
  });

  test('settings repository updates settings', () async {
    final repo = SettingsRepositoryImpl(_FakeSettingsDatasource());
    final updated = await repo.updateSettings(language: 'de');
    expect(updated.language, 'de');
  });
}
