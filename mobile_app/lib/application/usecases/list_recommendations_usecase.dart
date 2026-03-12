import '../../domain/entities/recommendation_entity.dart';
import '../../domain/repositories/recommendation_repository.dart';

class ListRecommendationsUseCase {
  const ListRecommendationsUseCase(this._repository);

  final RecommendationRepository _repository;

  Future<List<RecommendationEntity>> call({String? status}) {
    return _repository.list(status: status);
  }
}
