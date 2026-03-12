import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/weight_repository_impl.dart';
import '../../domain/entities/weight_log_entity.dart';
import '../usecases/create_weight_usecase.dart';
import '../usecases/list_weights_usecase.dart';

final weightsProvider = AsyncNotifierProvider<WeightsController, List<WeightLogEntity>>(WeightsController.new);

class WeightsController extends AsyncNotifier<List<WeightLogEntity>> {
  @override
  Future<List<WeightLogEntity>> build() async {
    final usecase = ListWeightsUseCase(ref.read(weightRepositoryProvider));
    return usecase();
  }

  Future<void> addWeight(double weightKg) async {
    final create = CreateWeightUseCase(ref.read(weightRepositoryProvider));
    await create(weightKg, DateTime.now().toUtc());
    final list = ListWeightsUseCase(ref.read(weightRepositoryProvider));
    state = await AsyncValue.guard(() => list());
  }
}
