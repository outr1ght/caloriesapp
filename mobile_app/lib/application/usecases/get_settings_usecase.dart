import '../../domain/entities/user_settings_entity.dart';
import '../../domain/repositories/settings_repository.dart';

class GetSettingsUseCase {
  const GetSettingsUseCase(this._repository);

  final SettingsRepository _repository;

  Future<UserSettingsEntity> call() {
    return _repository.getSettings();
  }
}
