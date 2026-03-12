class UploadEntity {
  const UploadEntity({
    required this.uploadId,
    required this.imageId,
    required this.storageKey,
    required this.status,
  });

  final String uploadId;
  final String imageId;
  final String storageKey;
  final String status;
}
