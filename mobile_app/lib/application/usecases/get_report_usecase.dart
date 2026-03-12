import '../../domain/entities/nutrition_report_entity.dart';
import '../../domain/entities/report_period.dart';
import '../../domain/repositories/report_repository.dart';

class GetReportUseCase {
  const GetReportUseCase(this._repository);

  final ReportRepository _repository;

  Future<NutritionReportEntity> call(ReportPeriod period) {
    switch (period) {
      case ReportPeriod.daily:
        return _repository.getDaily();
      case ReportPeriod.weekly:
        return _repository.getWeekly();
      case ReportPeriod.monthly:
        return _repository.getMonthly();
    }
  }
}
