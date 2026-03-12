import '../../domain/entities/weight_log_entity.dart';
import '../../domain/repositories/weight_repository.dart';

class CreateWeightUseCase {
  const CreateWeightUseCase(this._repository);

  final WeightRepository _repository;

  Future<WeightLogEntity> call(double weightKg, DateTime loggedAt) {
    return _repository.create(weightKg, loggedAt);
  }
}
