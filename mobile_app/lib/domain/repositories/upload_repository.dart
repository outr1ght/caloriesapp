import '../entities/upload_entity.dart';

abstract class UploadRepository {
  Future<UploadEntity> uploadImage(String filePath, {String? mealId});
}
