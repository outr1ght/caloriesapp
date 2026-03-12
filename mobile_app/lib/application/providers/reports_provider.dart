import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/report_repository_impl.dart';
import '../../domain/entities/nutrition_report_entity.dart';
import '../../domain/entities/report_period.dart';
import '../usecases/get_report_usecase.dart';

final reportsPeriodProvider = StateProvider<ReportPeriod>((_) => ReportPeriod.daily);

final reportsProvider = AsyncNotifierProvider<ReportsController, NutritionReportEntity>(ReportsController.new);

class ReportsController extends AsyncNotifier<NutritionReportEntity> {
  @override
  Future<NutritionReportEntity> build() async {
    final period = ref.watch(reportsPeriodProvider);
    final usecase = GetReportUseCase(ref.read(reportRepositoryProvider));
    return usecase(period);
  }

  Future<void> setPeriod(ReportPeriod period) async {
    ref.read(reportsPeriodProvider.notifier).state = period;
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = GetReportUseCase(ref.read(reportRepositoryProvider));
      return usecase(period);
    });
  }
}
