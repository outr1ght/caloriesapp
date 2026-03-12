import '../../domain/entities/user_settings_entity.dart';
import '../../domain/repositories/settings_repository.dart';

class UpdateSettingsUseCase {
  const UpdateSettingsUseCase(this._repository);

  final SettingsRepository _repository;

  Future<UserSettingsEntity> call({
    String? language,
    String? unitSystem,
    bool? notificationsEnabled,
    bool? mealReminderEnabled,
  }) {
    return _repository.updateSettings(
      language: language,
      unitSystem: unitSystem,
      notificationsEnabled: notificationsEnabled,
      mealReminderEnabled: mealReminderEnabled,
    );
  }
}
