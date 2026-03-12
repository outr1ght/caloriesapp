class ProfileEntity {
  const ProfileEntity({
    required this.firstName,
    required this.lastName,
    required this.age,
    required this.gender,
    required this.heightCm,
    required this.weightKg,
    required this.activityLevel,
  });

  final String firstName;
  final String lastName;
  final int age;
  final String gender;
  final double heightCm;
  final double weightKg;
  final String activityLevel;
}
