import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/meal_analysis_repository_impl.dart';
import '../../domain/entities/meal_analysis_entity.dart';
import '../usecases/analyze_meal_usecase.dart';
import '../usecases/save_meal_from_analysis_usecase.dart';

final mealAnalysisProvider = AsyncNotifierProvider<MealAnalysisController, MealAnalysisEntity?>(
  MealAnalysisController.new,
);

class MealAnalysisController extends AsyncNotifier<MealAnalysisEntity?> {
  @override
  Future<MealAnalysisEntity?> build() async {
    return null;
  }

  Future<void> analyze(String uploadedImageId) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = AnalyzeMealUseCase(ref.read(mealAnalysisRepositoryProvider));
      return usecase(uploadedImageId);
    });
  }

  void updateItemName(int index, String value) {
    final current = state.valueOrNull;
    if (current == null) return;
    if (index < 0 || index >= current.items.length) return;

    final normalized = value.trim();
    final nextItems = [...current.items];
    nextItems[index] = nextItems[index].copyWith(name: normalized);
    state = AsyncData(current.copyWith(items: nextItems));
  }

  bool hasInvalidItems() {
    final current = state.valueOrNull;
    if (current == null || current.items.isEmpty) return true;
    return current.items.any((x) => x.name.trim().isEmpty || x.quantity <= 0);
  }

  Future<String?> saveMeal() async {
    final current = state.valueOrNull;
    if (current == null) return null;

    final sanitized = current.copyWith(
      items: current.items.where((x) => x.name.trim().isNotEmpty && x.quantity > 0).toList(),
    );
    if (sanitized.items.isEmpty) {
      throw StateError('invalid_ingredients');
    }

    final usecase = SaveMealFromAnalysisUseCase(ref.read(mealAnalysisRepositoryProvider));
    final mealId = await usecase(sanitized);
    return mealId;
  }
}
