import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/weights_api_datasource.dart';
import 'package:calories_mobile/data/repositories/weight_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeWeightsDatasource extends WeightsApiDatasource {
  _FakeWeightsDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> list({int page = 1, int pageSize = 30}) async => {
    'data': {
      'items': [
        {'id': 'w1', 'logged_at': '2026-01-01T00:00:00Z', 'weight_kg': '75.2'}
      ]
    }
  };

  @override
  Future<Map<String, dynamic>> create({required double weightKg, required DateTime loggedAt}) async => {
    'data': {'id': 'w2', 'logged_at': '2026-01-02T00:00:00Z', 'weight_kg': weightKg.toString()}
  };
}

void main() {
  test('weight repository maps list', () async {
    final repo = WeightRepositoryImpl(_FakeWeightsDatasource());
    final items = await repo.list();
    expect(items.first.weightKg, 75.2);
  });

  test('weight repository creates entry', () async {
    final repo = WeightRepositoryImpl(_FakeWeightsDatasource());
    final item = await repo.create(76.0, DateTime.utc(2026, 1, 2));
    expect(item.weightKg, 76.0);
  });
}
