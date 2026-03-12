import '../../domain/entities/weight_log_entity.dart';

class WeightLogModel {
  const WeightLogModel({required this.id, required this.loggedAt, required this.weightKg});

  final String id;
  final DateTime loggedAt;
  final double weightKg;

  factory WeightLogModel.fromJson(Map<String, dynamic> json) {
    final rawWeight = json['weight_kg'];
    double weight = 0;
    if (rawWeight is num) {
      weight = rawWeight.toDouble();
    } else if (rawWeight is String) {
      weight = double.tryParse(rawWeight) ?? 0;
    }

    return WeightLogModel(
      id: (json['id'] as String?) ?? '',
      loggedAt: DateTime.tryParse((json['logged_at'] as String?) ?? '')?.toUtc() ?? DateTime.now().toUtc(),
      weightKg: weight,
    );
  }

  WeightLogEntity toEntity() {
    return WeightLogEntity(id: id, loggedAt: loggedAt, weightKg: weightKg);
  }
}
