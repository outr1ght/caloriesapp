import '../../domain/entities/weight_log_entity.dart';
import '../../domain/repositories/weight_repository.dart';

class ListWeightsUseCase {
  const ListWeightsUseCase(this._repository);

  final WeightRepository _repository;

  Future<List<WeightLogEntity>> call() {
    return _repository.list();
  }
}
