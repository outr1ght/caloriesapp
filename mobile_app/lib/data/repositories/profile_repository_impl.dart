import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/profile_entity.dart';
import '../../domain/repositories/profile_repository.dart';
import '../datasources/profile_api_datasource.dart';
import '../models/profile_models.dart';
import '../models/weight_models.dart';

final profileApiDatasourceProvider = Provider<ProfileApiDatasource>((ref) {
  return ProfileApiDatasource(ref.read(apiClientProvider));
});

final profileRepositoryProvider = Provider<ProfileRepository>((ref) {
  return ProfileRepositoryImpl(ref.read(profileApiDatasourceProvider));
});

class ProfileRepositoryImpl implements ProfileRepository {
  ProfileRepositoryImpl(this._datasource);

  final ProfileApiDatasource _datasource;

  @override
  Future<ProfileEntity?> getProfile() async {
    final me = await _datasource.getMe();
    final weightRoot = await _datasource.listWeights();
    final activity = await _datasource.getActivityLevel();

    final wData = (weightRoot['data'] as Map<String, dynamic>?) ?? weightRoot;
    final items = (wData['items'] as List<dynamic>? ?? const []).whereType<Map<String, dynamic>>().toList();
    final weight = items.isEmpty ? 0 : WeightLogModel.fromJson(items.first).weightKg;

    final model = ProfileModel.fromApi(me, weightKg: weight, activityLevel: activity);

    if (model.firstName.isEmpty && model.heightCm <= 0 && model.birthYear == null) {
      return null;
    }

    return model.toEntity();
  }

  @override
  Future<bool> isCompleted() async {
    final profile = await getProfile();
    if (profile == null) return false;
    return profile.firstName.isNotEmpty && profile.age > 0 && profile.heightCm > 0;
  }

  @override
  Future<void> saveProfile(ProfileEntity profile) async {
    await _datasource.updateProfile(
      firstName: profile.firstName,
      lastName: profile.lastName,
      age: profile.age,
      gender: profile.gender,
      heightCm: profile.heightCm,
    );
    if (profile.weightKg > 0) {
      await _datasource.createWeight(profile.weightKg);
    }
    await _datasource.saveActivityLevel(profile.activityLevel);
  }
}
