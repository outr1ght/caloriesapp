import 'profile_setup.dart';

abstract class ProfileSetupRepository {
  Future<ProfileSetup?> load();
  Future<void> save(ProfileSetup profile);
}
