class ProfileSetup {
  const ProfileSetup({
    required this.name,
    required this.age,
    required this.heightCm,
    required this.weightKg,
  });

  final String name;
  final int age;
  final double heightCm;
  final double weightKg;

  Map<String, dynamic> toJson() => {
        'name': name,
        'age': age,
        'height_cm': heightCm,
        'weight_kg': weightKg,
      };

  static ProfileSetup fromJson(Map<String, dynamic> json) {
    return ProfileSetup(
      name: (json['name'] as String?) ?? '',
      age: (json['age'] as num?)?.toInt() ?? 0,
      heightCm: (json['height_cm'] as num?)?.toDouble() ?? 0,
      weightKg: (json['weight_kg'] as num?)?.toDouble() ?? 0,
    );
  }
}
