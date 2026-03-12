import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/meal_analysis_provider.dart';
import 'package:calories_mobile/data/repositories/meal_analysis_repository_impl.dart';
import 'package:calories_mobile/domain/entities/meal_analysis_entity.dart';
import 'package:calories_mobile/domain/repositories/meal_analysis_repository.dart';

class _FakeMealAnalysisRepository implements MealAnalysisRepository {
  @override
  Future<MealAnalysisEntity> analyze(String uploadedImageId, {String? mealId}) async {
    return const MealAnalysisEntity(
      mealId: 'm1',
      status: 'ready',
      items: [MealAnalysisItemEntity(name: 'Rice', quantity: 100, unit: 'g', confidence: 0.8)],
      calories: 200,
      protein: 4,
      carbs: 40,
      fat: 1,
      confidence: 0.8,
      explanation: 'ok',
      warnings: [],
    );
  }

  @override
  Future<String> saveMealFromAnalysis(MealAnalysisEntity analysis, {String mealType = 'lunch'}) async {
    return 'meal_saved';
  }
}

void main() {
  test('meal analysis provider analyze and save', () async {
    final fake = _FakeMealAnalysisRepository();
    final container = ProviderContainer(overrides: [mealAnalysisRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(mealAnalysisProvider.future);
    await container.read(mealAnalysisProvider.notifier).analyze('img1');

    final state = container.read(mealAnalysisProvider).valueOrNull;
    expect(state?.items.first.name, 'Rice');

    final saved = await container.read(mealAnalysisProvider.notifier).saveMeal();
    expect(saved, 'meal_saved');
  });

  test('meal analysis provider rejects empty ingredient names', () async {
    final fake = _FakeMealAnalysisRepository();
    final container = ProviderContainer(overrides: [mealAnalysisRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(mealAnalysisProvider.future);
    await container.read(mealAnalysisProvider.notifier).analyze('img1');
    container.read(mealAnalysisProvider.notifier).updateItemName(0, '   ');

    expect(container.read(mealAnalysisProvider.notifier).hasInvalidItems(), isTrue);
  });
}
