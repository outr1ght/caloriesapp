import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/meal_capture_provider.dart';
import 'package:calories_mobile/data/repositories/upload_repository_impl.dart';
import 'package:calories_mobile/domain/entities/upload_entity.dart';
import 'package:calories_mobile/domain/repositories/upload_repository.dart';

class _FakeUploadRepository implements UploadRepository {
  @override
  Future<UploadEntity> uploadImage(String filePath, {String? mealId}) async {
    return const UploadEntity(uploadId: 'u1', imageId: 'img1', storageKey: 'k1', status: 'uploaded');
  }
}

void main() {
  test('meal capture provider upload succeeds', () async {
    final fake = _FakeUploadRepository();
    final container = ProviderContainer(overrides: [uploadRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(mealCaptureProvider.future);
    await container.read(mealCaptureProvider.notifier).upload('path.jpg');

    expect(container.read(mealCaptureProvider).valueOrNull?.imageId, 'img1');
  });
}
