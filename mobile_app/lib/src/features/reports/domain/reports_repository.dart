import 'report_summary.dart';

abstract class ReportsRepository {
  Future<ReportSummary> getWeekly();
}
