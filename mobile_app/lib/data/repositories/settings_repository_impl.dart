import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/user_settings_entity.dart';
import '../../domain/repositories/settings_repository.dart';
import '../datasources/settings_api_datasource.dart';
import '../models/settings_models.dart';

final settingsApiDatasourceProvider = Provider<SettingsApiDatasource>((ref) {
  return SettingsApiDatasource(ref.read(apiClientProvider));
});

final settingsRepositoryProvider = Provider<SettingsRepository>((ref) {
  return SettingsRepositoryImpl(ref.read(settingsApiDatasourceProvider));
});

class SettingsRepositoryImpl implements SettingsRepository {
  SettingsRepositoryImpl(this._datasource);

  final SettingsApiDatasource _datasource;

  @override
  Future<UserSettingsEntity> getSettings() async {
    final root = await _datasource.getSettings();
    return UserSettingsModel.fromApi(root).toEntity();
  }

  @override
  Future<UserSettingsEntity> updateSettings({
    String? language,
    String? unitSystem,
    bool? notificationsEnabled,
    bool? mealReminderEnabled,
  }) async {
    final payload = <String, dynamic>{};
    if (language != null) payload['language'] = language;
    if (unitSystem != null) payload['unit_system'] = unitSystem;
    if (notificationsEnabled != null) payload['notifications_enabled'] = notificationsEnabled;
    if (mealReminderEnabled != null) payload['meal_reminder_enabled'] = mealReminderEnabled;

    final root = await _datasource.patchSettings(payload);
    return UserSettingsModel.fromApi(root).toEntity();
  }
}
