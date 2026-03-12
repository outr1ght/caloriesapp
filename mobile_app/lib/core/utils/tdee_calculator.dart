class TdeeCalculator {
  static int estimate({
    required int age,
    required double heightCm,
    required double weightKg,
    required String gender,
    required String activityLevel,
  }) {
    final isMale = gender.toLowerCase() == 'male';
    final bmr = (10 * weightKg) + (6.25 * heightCm) - (5 * age) + (isMale ? 5 : -161);
    final multiplier = switch (activityLevel) {
      'sedentary' => 1.2,
      'light' => 1.375,
      'moderate' => 1.55,
      'active' => 1.725,
      'very_active' => 1.9,
      _ => 1.55,
    };

    return (bmr * multiplier).round().clamp(1200, 6000);
  }
}
