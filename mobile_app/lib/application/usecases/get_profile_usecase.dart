import '../../domain/entities/profile_entity.dart';
import '../../domain/repositories/profile_repository.dart';

class GetProfileUseCase {
  const GetProfileUseCase(this._repository);

  final ProfileRepository _repository;

  Future<ProfileEntity?> call() {
    return _repository.getProfile();
  }
}
