import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/recommendations_api_datasource.dart';
import 'package:calories_mobile/data/repositories/recommendation_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeRecommendationsDatasource extends RecommendationsApiDatasource {
  _FakeRecommendationsDatasource() : super(DummyApiClient());

  bool updated = false;

  @override
  Future<Map<String, dynamic>> list({String? status, int page = 1, int pageSize = 20}) async => {
    'data': {
      'items': [
        {'id': 'r1', 'title': 'Protein', 'status': 'ready', 'type': 'goal_alignment'}
      ]
    }
  };

  @override
  Future<void> updateStatus(String id, String status) async {
    updated = true;
  }
}

void main() {
  test('recommendation repository maps list', () async {
    final ds = _FakeRecommendationsDatasource();
    final repo = RecommendationRepositoryImpl(ds);
    final items = await repo.list();
    expect(items.length, 1);
    expect(items.first.status, 'ready');
  });

  test('recommendation repository updates status', () async {
    final ds = _FakeRecommendationsDatasource();
    final repo = RecommendationRepositoryImpl(ds);
    await repo.updateStatus('r1', 'applied');
    expect(ds.updated, isTrue);
  });
}
