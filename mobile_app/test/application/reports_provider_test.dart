import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/reports_provider.dart';
import 'package:calories_mobile/data/repositories/report_repository_impl.dart';
import 'package:calories_mobile/domain/entities/nutrition_report_entity.dart';
import 'package:calories_mobile/domain/entities/report_period.dart';
import 'package:calories_mobile/domain/repositories/report_repository.dart';

class _FakeReportRepository implements ReportRepository {
  @override
  Future<NutritionReportEntity> getDaily() async => const NutritionReportEntity(
    totalCalories: 1000,
    averageCalories: 1000,
    protein: 50,
    carbs: 120,
    fat: 40,
    trend: [ReportPointEntity(label: 'd', calories: 1000)],
  );

  @override
  Future<NutritionReportEntity> getMonthly() async => const NutritionReportEntity(
    totalCalories: 30000,
    averageCalories: 1000,
    protein: 1500,
    carbs: 3600,
    fat: 1200,
    trend: [ReportPointEntity(label: 'm', calories: 1000)],
  );

  @override
  Future<NutritionReportEntity> getWeekly() async => const NutritionReportEntity(
    totalCalories: 7000,
    averageCalories: 1000,
    protein: 350,
    carbs: 840,
    fat: 280,
    trend: [ReportPointEntity(label: 'w', calories: 1000)],
  );
}

void main() {
  test('reports provider switches period', () async {
    final fake = _FakeReportRepository();
    final container = ProviderContainer(overrides: [reportRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    final initial = await container.read(reportsProvider.future);
    expect(initial.totalCalories, 1000);

    await container.read(reportsProvider.notifier).setPeriod(ReportPeriod.weekly);
    final next = container.read(reportsProvider).valueOrNull;
    expect(next?.totalCalories, 7000);
  });
}
