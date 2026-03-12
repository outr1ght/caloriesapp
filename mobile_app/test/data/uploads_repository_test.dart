import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/datasources/uploads_api_datasource.dart';
import 'package:calories_mobile/data/repositories/upload_repository_impl.dart';

import '../helpers/test_helpers.dart';

class _FakeUploadsDatasource extends UploadsApiDatasource {
  _FakeUploadsDatasource() : super(DummyApiClient());

  bool uploaded = false;

  @override
  Future<Map<String, dynamic>> initUpload({required String filename, required String mimeType, required int fileSize, required String sha256, String? mealId}) async {
    return {
      'data': {
        'upload_id': 'u1',
        'storage_key': 'k1',
        'upload_url': 'https://example.com',
        'upload_headers': <String, String>{},
      }
    };
  }

  @override
  Future<void> uploadBinary({required String uploadUrl, required dynamic bytes, required String mimeType, required Map<String, dynamic> headers}) async {
    uploaded = true;
  }

  @override
  Future<Map<String, dynamic>> completeUpload(String uploadId) async => {
    'data': {'id': 'img1', 'storage_key': 'k1', 'status': 'uploaded'}
  };
}

void main() {
  test('upload repository uploads and completes', () async {
    final ds = _FakeUploadsDatasource();
    final repo = UploadRepositoryImpl(ds);

    final dir = await Directory.systemTemp.createTemp('upload_repo_test');
    final file = File('${dir.path}/sample.jpg');
    await file.writeAsBytes([1, 2, 3, 4]);

    final result = await repo.uploadImage(file.path);

    expect(ds.uploaded, isTrue);
    expect(result.imageId, 'img1');

    await dir.delete(recursive: true);
  });
}
