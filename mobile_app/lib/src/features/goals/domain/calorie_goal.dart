class CalorieGoal {
  const CalorieGoal({
    required this.dailyCalories,
    required this.proteinGrams,
    required this.carbsGrams,
    required this.fatGrams,
  });

  final int dailyCalories;
  final int proteinGrams;
  final int carbsGrams;
  final int fatGrams;

  Map<String, dynamic> toJson() => {
        'daily_calories': dailyCalories,
        'protein_grams': proteinGrams,
        'carbs_grams': carbsGrams,
        'fat_grams': fatGrams,
      };

  static CalorieGoal fromJson(Map<String, dynamic> json) {
    return CalorieGoal(
      dailyCalories: (json['daily_calories'] as num?)?.toInt() ?? 2000,
      proteinGrams: (json['protein_grams'] as num?)?.toInt() ?? 120,
      carbsGrams: (json['carbs_grams'] as num?)?.toInt() ?? 200,
      fatGrams: (json['fat_grams'] as num?)?.toInt() ?? 70,
    );
  }
}
