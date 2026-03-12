import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/barcode_api_datasource.dart';
import 'package:calories_mobile/data/repositories/barcode_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeBarcodeDatasource extends BarcodeApiDatasource {
  _FakeBarcodeDatasource() : super(DummyApiClient());

  @override
  Future<Map<String, dynamic>> lookup(String code) async => {
    'data': {
      'found': true,
      'product': {'product_id': 'p1', 'name': 'Apple', 'brand': 'Brand', 'barcode': code}
    }
  };

  @override
  Future<Map<String, dynamic>> saveAsMeal(String name) async => {
    'data': {'id': 'meal1'}
  };
}

void main() {
  test('barcode repository lookup maps product', () async {
    final repo = BarcodeRepositoryImpl(_FakeBarcodeDatasource());
    final result = await repo.lookup('1234');
    expect(result.found, isTrue);
    expect(result.product?.name, 'Apple');
  });

  test('barcode repository saves meal', () async {
    final repo = BarcodeRepositoryImpl(_FakeBarcodeDatasource());
    final result = await repo.lookup('1234');
    final mealId = await repo.saveAsMeal(result.product!);
    expect(mealId, 'meal1');
  });
}
