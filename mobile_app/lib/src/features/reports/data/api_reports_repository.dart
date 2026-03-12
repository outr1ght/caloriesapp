import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/api_client.dart';
import '../../../core/network/dio_client.dart';
import '../domain/report_summary.dart';
import '../domain/reports_repository.dart';

final reportsRepositoryProvider = Provider<ReportsRepository>((ref) {
  return ApiReportsRepository(ref.read(apiClientProvider));
});

class ApiReportsRepository implements ReportsRepository {
  ApiReportsRepository(this._apiClient);

  final ApiClient _apiClient;

  @override
  Future<ReportSummary> getWeekly() async {
    final response = await _apiClient.get<Map<String, dynamic>>('/reports/weekly');
    final data = response.data ?? <String, dynamic>{};
    return ReportSummary(
      period: (data['period'] as String?) ?? 'weekly',
      calories: ((data['calories'] as num?) ?? 0).toDouble(),
      proteinG: ((data['protein_g'] as num?) ?? 0).toDouble(),
      fatG: ((data['fat_g'] as num?) ?? 0).toDouble(),
      carbsG: ((data['carbs_g'] as num?) ?? 0).toDouble(),
    );
  }
}
