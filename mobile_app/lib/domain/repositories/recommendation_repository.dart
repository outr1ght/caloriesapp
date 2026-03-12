import '../entities/recommendation_entity.dart';

abstract class RecommendationRepository {
  Future<List<RecommendationEntity>> list({String? status});
  Future<void> updateStatus(String id, String status);
}
