import '../../domain/entities/user_settings_entity.dart';

class UserSettingsModel {
  const UserSettingsModel({
    required this.id,
    required this.userId,
    required this.language,
    required this.unitSystem,
    required this.notificationsEnabled,
    required this.mealReminderEnabled,
  });

  final String id;
  final String userId;
  final String language;
  final String unitSystem;
  final bool notificationsEnabled;
  final bool mealReminderEnabled;

  factory UserSettingsModel.fromApi(Map<String, dynamic> root) {
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return UserSettingsModel(
      id: (data['id'] as String?) ?? '',
      userId: (data['user_id'] as String?) ?? '',
      language: (data['language'] as String?) ?? 'en',
      unitSystem: (data['unit_system'] as String?) ?? 'metric',
      notificationsEnabled: (data['notifications_enabled'] as bool?) ?? true,
      mealReminderEnabled: (data['meal_reminder_enabled'] as bool?) ?? false,
    );
  }

  UserSettingsEntity toEntity() {
    return UserSettingsEntity(
      id: id,
      userId: userId,
      language: language,
      unitSystem: unitSystem,
      notificationsEnabled: notificationsEnabled,
      mealReminderEnabled: mealReminderEnabled,
    );
  }
}
