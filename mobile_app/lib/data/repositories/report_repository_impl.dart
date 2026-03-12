import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/nutrition_report_entity.dart';
import '../../domain/repositories/report_repository.dart';
import '../datasources/reports_api_datasource.dart';
import '../models/report_models.dart';

final reportsApiDatasourceProvider = Provider<ReportsApiDatasource>((ref) {
  return ReportsApiDatasource(ref.read(apiClientProvider));
});

final reportRepositoryProvider = Provider<ReportRepository>((ref) {
  return ReportRepositoryImpl(ref.read(reportsApiDatasourceProvider));
});

class ReportRepositoryImpl implements ReportRepository {
  ReportRepositoryImpl(this._datasource);

  final ReportsApiDatasource _datasource;

  @override
  Future<NutritionReportEntity> getDaily() async {
    final now = DateTime.now().toUtc();
    final json = await _datasource.fetchNutrition(from: now, to: now);
    return NutritionReportModel.fromApi(json).toEntity();
  }

  @override
  Future<NutritionReportEntity> getWeekly() async {
    final now = DateTime.now().toUtc();
    final from = now.subtract(const Duration(days: 6));
    final json = await _datasource.fetchNutrition(from: from, to: now);
    return NutritionReportModel.fromApi(json).toEntity();
  }

  @override
  Future<NutritionReportEntity> getMonthly() async {
    final now = DateTime.now().toUtc();
    final from = now.subtract(const Duration(days: 29));
    final json = await _datasource.fetchNutrition(from: from, to: now);
    return NutritionReportModel.fromApi(json).toEntity();
  }
}
