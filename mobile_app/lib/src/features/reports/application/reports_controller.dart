import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/api_reports_repository.dart';
import '../domain/report_summary.dart';

final reportsControllerProvider = AsyncNotifierProvider<ReportsController, ReportSummary>(ReportsController.new);

class ReportsController extends AsyncNotifier<ReportSummary> {
  @override
  Future<ReportSummary> build() async {
    return ref.read(reportsRepositoryProvider).getWeekly();
  }

  Future<void> refreshReport() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => ref.read(reportsRepositoryProvider).getWeekly());
  }
}
