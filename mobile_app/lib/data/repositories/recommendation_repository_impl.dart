import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/recommendation_entity.dart';
import '../../domain/repositories/recommendation_repository.dart';
import '../datasources/recommendations_api_datasource.dart';
import '../models/recommendation_models.dart';

final recommendationsApiDatasourceProvider = Provider<RecommendationsApiDatasource>((ref) {
  return RecommendationsApiDatasource(ref.read(apiClientProvider));
});

final recommendationRepositoryProvider = Provider<RecommendationRepository>((ref) {
  return RecommendationRepositoryImpl(ref.read(recommendationsApiDatasourceProvider));
});

class RecommendationRepositoryImpl implements RecommendationRepository {
  RecommendationRepositoryImpl(this._datasource);

  final RecommendationsApiDatasource _datasource;

  @override
  Future<List<RecommendationEntity>> list({String? status}) async {
    final root = await _datasource.list(status: status);
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    final items = (data['items'] as List<dynamic>? ?? const []).whereType<Map<String, dynamic>>();
    return items.map((x) => RecommendationModel.fromJson(x).toEntity()).toList();
  }

  @override
  Future<void> updateStatus(String id, String status) {
    return _datasource.updateStatus(id, status);
  }
}
