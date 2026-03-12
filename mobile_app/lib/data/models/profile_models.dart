import '../../domain/entities/profile_entity.dart';

class ProfileModel {
  const ProfileModel({
    required this.firstName,
    required this.lastName,
    required this.birthYear,
    required this.gender,
    required this.heightCm,
    required this.weightKg,
    required this.activityLevel,
  });

  final String firstName;
  final String lastName;
  final int? birthYear;
  final String gender;
  final double heightCm;
  final double weightKg;
  final String activityLevel;

  factory ProfileModel.fromApi(Map<String, dynamic> meRoot, {double weightKg = 0, String activityLevel = 'moderate'}) {
    final meData = (meRoot['data'] as Map<String, dynamic>?) ?? meRoot;
    final profile = (meData['profile'] as Map<String, dynamic>?) ?? const {};

    return ProfileModel(
      firstName: (profile['first_name'] as String?) ?? '',
      lastName: (profile['last_name'] as String?) ?? '',
      birthYear: (profile['birth_year'] as num?)?.toInt(),
      gender: (profile['gender'] as String?) ?? 'male',
      heightCm: ((profile['height_cm'] as num?) ?? 0).toDouble(),
      weightKg: weightKg,
      activityLevel: activityLevel,
    );
  }

  ProfileEntity toEntity() {
    final nowYear = DateTime.now().year;
    final age = birthYear == null ? 0 : (nowYear - birthYear!).clamp(0, 120);
    return ProfileEntity(
      firstName: firstName,
      lastName: lastName,
      age: age,
      gender: gender,
      heightCm: heightCm,
      weightKg: weightKg,
      activityLevel: activityLevel,
    );
  }
}
