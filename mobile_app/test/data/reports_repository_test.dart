import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/reports_api_datasource.dart';
import 'package:calories_mobile/data/repositories/report_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeReportsDatasource extends ReportsApiDatasource {
  _FakeReportsDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> fetchNutrition({required DateTime from, required DateTime to}) async => {
    'data': {
      'totals_calories': 2000,
      'avg_daily_calories': 2000,
      'days': [
        {
          'date': '2026-01-01',
          'calories': 2000,
          'macros': {'protein_g': 100, 'carbs_g': 220, 'fat_g': 70}
        }
      ]
    }
  };
}

void main() {
  test('report repository maps nutrition report', () async {
    final repo = ReportRepositoryImpl(_FakeReportsDatasource());
    final daily = await repo.getDaily();
    expect(daily.totalCalories, 2000);
    expect(daily.trend.length, 1);
  });
}
