import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/local_profile_setup_repository.dart';
import '../domain/profile_setup.dart';

final profileSetupControllerProvider = AsyncNotifierProvider<ProfileSetupController, ProfileSetup?>(ProfileSetupController.new);

class ProfileSetupController extends AsyncNotifier<ProfileSetup?> {
  @override
  Future<ProfileSetup?> build() async {
    return ref.read(profileSetupRepositoryProvider).load();
  }

  Future<void> save(ProfileSetup profile) async {
    await ref.read(profileSetupRepositoryProvider).save(profile);
    state = AsyncData(profile);
  }
}
