import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/settings_repository_impl.dart';
import '../../domain/entities/user_settings_entity.dart';
import '../usecases/get_settings_usecase.dart';
import '../usecases/update_settings_usecase.dart';

final settingsProvider = AsyncNotifierProvider<SettingsController, UserSettingsEntity>(SettingsController.new);

class SettingsController extends AsyncNotifier<UserSettingsEntity> {
  @override
  Future<UserSettingsEntity> build() async {
    final usecase = GetSettingsUseCase(ref.read(settingsRepositoryProvider));
    return usecase();
  }

  Future<void> updateLanguage(String language) async {
    final usecase = UpdateSettingsUseCase(ref.read(settingsRepositoryProvider));
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => usecase(language: language));
  }

  Future<void> updateUnitSystem(String unitSystem) async {
    final usecase = UpdateSettingsUseCase(ref.read(settingsRepositoryProvider));
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => usecase(unitSystem: unitSystem));
  }

  Future<void> updateNotifications(bool enabled) async {
    final usecase = UpdateSettingsUseCase(ref.read(settingsRepositoryProvider));
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => usecase(notificationsEnabled: enabled));
  }

  Future<void> updateMealReminder(bool enabled) async {
    final usecase = UpdateSettingsUseCase(ref.read(settingsRepositoryProvider));
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => usecase(mealReminderEnabled: enabled));
  }
}
