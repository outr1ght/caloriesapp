import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/recommendation_repository_impl.dart';
import '../../domain/entities/recommendation_entity.dart';
import '../usecases/list_recommendations_usecase.dart';
import '../usecases/update_recommendation_status_usecase.dart';

final recommendationsProvider = AsyncNotifierProvider<RecommendationsController, List<RecommendationEntity>>(
  RecommendationsController.new,
);

class RecommendationsController extends AsyncNotifier<List<RecommendationEntity>> {
  @override
  Future<List<RecommendationEntity>> build() async {
    final usecase = ListRecommendationsUseCase(ref.read(recommendationRepositoryProvider));
    return usecase();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = ListRecommendationsUseCase(ref.read(recommendationRepositoryProvider));
      return usecase();
    });
  }

  Future<void> markApplied(String id) async {
    final update = UpdateRecommendationStatusUseCase(ref.read(recommendationRepositoryProvider));
    await update(id, 'applied');
    await refresh();
  }

  Future<void> dismiss(String id) async {
    final update = UpdateRecommendationStatusUseCase(ref.read(recommendationRepositoryProvider));
    await update(id, 'dismissed');
    await refresh();
  }
}
