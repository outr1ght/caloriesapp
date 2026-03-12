import '../entities/user_settings_entity.dart';

abstract class SettingsRepository {
  Future<UserSettingsEntity> getSettings();
  Future<UserSettingsEntity> updateSettings({
    String? language,
    String? unitSystem,
    bool? notificationsEnabled,
    bool? mealReminderEnabled,
  });
}
