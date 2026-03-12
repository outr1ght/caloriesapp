import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/upload_repository_impl.dart';
import '../../domain/entities/upload_entity.dart';
import '../usecases/upload_image_usecase.dart';

final mealCaptureProvider = AsyncNotifierProvider<MealCaptureController, UploadEntity?>(MealCaptureController.new);

class MealCaptureController extends AsyncNotifier<UploadEntity?> {
  @override
  Future<UploadEntity?> build() async {
    return null;
  }

  Future<void> upload(String filePath) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = UploadImageUseCase(ref.read(uploadRepositoryProvider));
      return usecase(filePath);
    });
  }
}
