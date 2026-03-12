import '../../domain/entities/profile_entity.dart';
import '../../domain/repositories/profile_repository.dart';

class SaveProfileUseCase {
  const SaveProfileUseCase(this._repository);

  final ProfileRepository _repository;

  Future<void> call(ProfileEntity profile) {
    return _repository.saveProfile(profile);
  }
}
