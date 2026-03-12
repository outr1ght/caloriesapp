import 'dart:convert';
import 'dart:io';

import 'package:crypto/crypto.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/upload_entity.dart';
import '../../domain/repositories/upload_repository.dart';
import '../datasources/uploads_api_datasource.dart';
import '../models/upload_models.dart';

final uploadsApiDatasourceProvider = Provider<UploadsApiDatasource>((ref) {
  return UploadsApiDatasource(ref.read(apiClientProvider));
});

final uploadRepositoryProvider = Provider<UploadRepository>((ref) {
  return UploadRepositoryImpl(ref.read(uploadsApiDatasourceProvider));
});

class UploadRepositoryImpl implements UploadRepository {
  UploadRepositoryImpl(this._datasource);

  final UploadsApiDatasource _datasource;

  @override
  Future<UploadEntity> uploadImage(String filePath, {String? mealId}) async {
    final file = File(filePath);
    final bytes = await file.readAsBytes();
    final filename = file.path.split(Platform.pathSeparator).last;
    final mimeType = _mimeByFilename(filename);
    final hash = sha256.convert(bytes).toString();

    final initRoot = await _datasource.initUpload(
      filename: filename,
      mimeType: mimeType,
      fileSize: bytes.length,
      sha256: hash,
      mealId: mealId,
    );

    final init = UploadInitModel.fromApi(initRoot);

    await _datasource.uploadBinary(
      uploadUrl: init.uploadUrl,
      bytes: bytes,
      mimeType: mimeType,
      headers: init.uploadHeaders,
    );

    final complete = UploadCompleteModel.fromApi(await _datasource.completeUpload(init.uploadId));
    return complete.toEntity(init.uploadId);
  }

  String _mimeByFilename(String filename) {
    final lower = filename.toLowerCase();
    if (lower.endsWith('.png')) return 'image/png';
    if (lower.endsWith('.webp')) return 'image/webp';
    return 'image/jpeg';
  }
}
