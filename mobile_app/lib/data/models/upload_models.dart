import '../../domain/entities/upload_entity.dart';

class UploadInitModel {
  const UploadInitModel({
    required this.uploadId,
    required this.storageKey,
    required this.uploadUrl,
    required this.uploadHeaders,
  });

  final String uploadId;
  final String storageKey;
  final String uploadUrl;
  final Map<String, dynamic> uploadHeaders;

  factory UploadInitModel.fromApi(Map<String, dynamic> root) {
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return UploadInitModel(
      uploadId: (data['upload_id'] as String?) ?? '',
      storageKey: (data['storage_key'] as String?) ?? '',
      uploadUrl: (data['upload_url'] as String?) ?? '',
      uploadHeaders: (data['upload_headers'] as Map<String, dynamic>?) ?? const {},
    );
  }
}

class UploadCompleteModel {
  const UploadCompleteModel({
    required this.imageId,
    required this.storageKey,
    required this.status,
  });

  final String imageId;
  final String storageKey;
  final String status;

  factory UploadCompleteModel.fromApi(Map<String, dynamic> root) {
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return UploadCompleteModel(
      imageId: (data['id'] as String?) ?? '',
      storageKey: (data['storage_key'] as String?) ?? '',
      status: (data['status'] as String?) ?? 'uploaded',
    );
  }

  UploadEntity toEntity(String uploadId) {
    return UploadEntity(
      uploadId: uploadId,
      imageId: imageId,
      storageKey: storageKey,
      status: status,
    );
  }
}
