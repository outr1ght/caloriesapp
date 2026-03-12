import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/barcode_lookup_entity.dart';
import '../../domain/repositories/barcode_repository.dart';
import '../datasources/barcode_api_datasource.dart';

final barcodeApiDatasourceProvider = Provider<BarcodeApiDatasource>((ref) {
  return BarcodeApiDatasource(ref.read(apiClientProvider));
});

final barcodeRepositoryProvider = Provider<BarcodeRepository>((ref) {
  return BarcodeRepositoryImpl(ref.read(barcodeApiDatasourceProvider));
});

class BarcodeRepositoryImpl implements BarcodeRepository {
  BarcodeRepositoryImpl(this._datasource);

  final BarcodeApiDatasource _datasource;

  @override
  Future<BarcodeLookupEntity> lookup(String code) async {
    final root = await _datasource.lookup(code);
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    final productData = data['product'] as Map<String, dynamic>?;

    return BarcodeLookupEntity(
      found: (data['found'] as bool?) ?? false,
      product: productData == null
          ? null
          : BarcodeProductEntity(
              productId: (productData['product_id'] as String?) ?? '',
              name: (productData['name'] as String?) ?? '',
              brand: (productData['brand'] as String?) ?? '',
              barcode: (productData['barcode'] as String?) ?? code,
            ),
    );
  }

  @override
  Future<String> saveAsMeal(BarcodeProductEntity product) async {
    final root = await _datasource.saveAsMeal(product.name);
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return (data['id'] as String?) ?? '';
  }
}
