import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/profile_repository_impl.dart';
import '../../domain/entities/profile_entity.dart';
import '../usecases/get_profile_usecase.dart';
import '../usecases/save_profile_usecase.dart';

final profileProvider = AsyncNotifierProvider<ProfileController, ProfileEntity?>(ProfileController.new);

class ProfileController extends AsyncNotifier<ProfileEntity?> {
  @override
  Future<ProfileEntity?> build() async {
    final usecase = GetProfileUseCase(ref.read(profileRepositoryProvider));
    return usecase();
  }

  Future<void> save(ProfileEntity profile) async {
    final usecase = SaveProfileUseCase(ref.read(profileRepositoryProvider));
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      await usecase(profile);
      return profile;
    });
  }

  Future<bool> isCompleted() {
    return ref.read(profileRepositoryProvider).isCompleted();
  }
}
