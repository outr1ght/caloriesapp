import '../entities/barcode_lookup_entity.dart';

abstract class BarcodeRepository {
  Future<BarcodeLookupEntity> lookup(String code);
  Future<String> saveAsMeal(BarcodeProductEntity product);
}
