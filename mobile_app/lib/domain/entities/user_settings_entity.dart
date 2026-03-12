class UserSettingsEntity {
  const UserSettingsEntity({
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
}
