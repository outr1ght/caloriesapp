import '../../domain/entities/barcode_lookup_entity.dart';
import '../../domain/repositories/barcode_repository.dart';

class SaveBarcodeMealUseCase {
  const SaveBarcodeMealUseCase(this._repository);

  final BarcodeRepository _repository;

  Future<String> call(BarcodeProductEntity product) {
    return _repository.saveAsMeal(product);
  }
}
