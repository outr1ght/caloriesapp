import '../entities/nutrition_report_entity.dart';

abstract class ReportRepository {
  Future<NutritionReportEntity> getDaily();
  Future<NutritionReportEntity> getWeekly();
  Future<NutritionReportEntity> getMonthly();
}
