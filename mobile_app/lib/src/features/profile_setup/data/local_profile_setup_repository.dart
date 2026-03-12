import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/storage/local_cache.dart';
import '../domain/profile_setup.dart';
import '../domain/profile_setup_repository.dart';

final localCacheProvider = Provider<LocalCache>((_) => LocalCache());

final profileSetupRepositoryProvider = Provider<ProfileSetupRepository>((ref) {
  return LocalProfileSetupRepository(ref.read(localCacheProvider));
});

class LocalProfileSetupRepository implements ProfileSetupRepository {
  LocalProfileSetupRepository(this._cache);

  final LocalCache _cache;
  static const _key = 'profile_setup_v1';

  @override
  Future<ProfileSetup?> load() async {
    final json = await _cache.readJson(_key);
    if (json == null) return null;
    return ProfileSetup.fromJson(json);
  }

  @override
  Future<void> save(ProfileSetup profile) async {
    await _cache.writeJson(_key, profile.toJson());
  }
}
