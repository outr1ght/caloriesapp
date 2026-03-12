import 'dart:typed_data';

import 'package:dio/dio.dart';

import '../../core/network/api_client.dart';

class UploadsApiDatasource {
  UploadsApiDatasource(this._client);

  final ApiClient _client;

  Future<Map<String, dynamic>> initUpload({
    required String filename,
    required String mimeType,
    required int fileSize,
    required String sha256,
    String? mealId,
  }) async {
    final response = await _client.post<Map<String, dynamic>>(
      '/uploads/init',
      data: {
        'filename': filename,
        'mime_type': mimeType,
        'file_size': fileSize,
        'sha256': sha256,
        'meal_id': mealId,
      },
    );
    return response.data ?? <String, dynamic>{};
  }

  Future<void> uploadBinary({
    required String uploadUrl,
    required Uint8List bytes,
    required String mimeType,
    required Map<String, dynamic> headers,
  }) async {
    final dio = Dio();
    await dio.put(
      uploadUrl,
      data: Stream.fromIterable([bytes]),
      options: Options(headers: {'Content-Type': mimeType, ...headers}, contentType: mimeType),
    );
  }

  Future<Map<String, dynamic>> completeUpload(String uploadId) async {
    final response = await _client.post<Map<String, dynamic>>('/uploads/complete', data: {'upload_id': uploadId});
    return response.data ?? <String, dynamic>{};
  }
}
