import '../../domain/entities/barcode_lookup_entity.dart';
import '../../domain/repositories/barcode_repository.dart';

class LookupBarcodeUseCase {
  const LookupBarcodeUseCase(this._repository);

  final BarcodeRepository _repository;

  Future<BarcodeLookupEntity> call(String code) {
    return _repository.lookup(code);
  }
}
