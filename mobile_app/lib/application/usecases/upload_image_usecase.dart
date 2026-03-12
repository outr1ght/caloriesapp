import '../../domain/entities/upload_entity.dart';
import '../../domain/repositories/upload_repository.dart';

class UploadImageUseCase {
  const UploadImageUseCase(this._repository);

  final UploadRepository _repository;

  Future<UploadEntity> call(String filePath, {String? mealId}) {
    return _repository.uploadImage(filePath, mealId: mealId);
  }
}
