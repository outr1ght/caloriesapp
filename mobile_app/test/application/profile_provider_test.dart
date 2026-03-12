import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/profile_provider.dart';
import 'package:calories_mobile/data/repositories/profile_repository_impl.dart';
import 'package:calories_mobile/domain/entities/profile_entity.dart';
import 'package:calories_mobile/domain/repositories/profile_repository.dart';

class _FakeProfileRepository implements ProfileRepository {
  ProfileEntity? _profile;

  @override
  Future<ProfileEntity?> getProfile() async => _profile;

  @override
  Future<bool> isCompleted() async => _profile != null;

  @override
  Future<void> saveProfile(ProfileEntity profile) async {
    _profile = profile;
  }
}

void main() {
  test('profile provider saves profile', () async {
    final fake = _FakeProfileRepository();
    final container = ProviderContainer(overrides: [profileRepositoryProvider.overrideWithValue(fake)]);
    addTearDown(container.dispose);

    await container.read(profileProvider.future);
    await container.read(profileProvider.notifier).save(const ProfileEntity(
      firstName: 'A',
      lastName: 'B',
      age: 30,
      gender: 'male',
      heightCm: 180,
      weightKg: 80,
      activityLevel: 'moderate',
    ));

    expect(container.read(profileProvider).valueOrNull?.firstName, 'A');
  });
}
