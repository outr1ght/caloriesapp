import '../entities/profile_entity.dart';

abstract class ProfileRepository {
  Future<ProfileEntity?> getProfile();
  Future<void> saveProfile(ProfileEntity profile);
  Future<bool> isCompleted();
}
