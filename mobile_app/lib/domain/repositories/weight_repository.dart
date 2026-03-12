import '../entities/weight_log_entity.dart';

abstract class WeightRepository {
  Future<List<WeightLogEntity>> list();
  Future<WeightLogEntity> create(double weightKg, DateTime loggedAt);
}
