import '../../domain/repositories/recommendation_repository.dart';

class UpdateRecommendationStatusUseCase {
  const UpdateRecommendationStatusUseCase(this._repository);

  final RecommendationRepository _repository;

  Future<void> call(String id, String status) {
    return _repository.updateStatus(id, status);
  }
}
