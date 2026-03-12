import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/barcode_provider.dart';
import 'package:calories_mobile/data/repositories/barcode_repository_impl.dart';
import 'package:calories_mobile/domain/entities/barcode_lookup_entity.dart';
import 'package:calories_mobile/domain/repositories/barcode_repository.dart';

class _FakeBarcodeRepository implements BarcodeRepository {
  @override
  Future<BarcodeLookupEntity> lookup(String code) async {
    return BarcodeLookupEntity(
      found: true,
      product: BarcodeProductEntity(productId: 'p1', name: 'Apple', brand: 'Brand', barcode: code),
    );
  }

  @override
  Future<String> saveAsMeal(BarcodeProductEntity product) async => 'meal1';
}

void main() {
  test('barcode provider lookup and save', () async {
    final fake = _FakeBarcodeRepository();
    final container = ProviderContainer(overrides: [barcodeRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(barcodeProvider.future);
    await container.read(barcodeProvider.notifier).lookup('123456');

    expect(container.read(barcodeProvider).valueOrNull?.product?.name, 'Apple');
    final mealId = await container.read(barcodeProvider.notifier).saveAsMeal();
    expect(mealId, 'meal1');
  });
}
