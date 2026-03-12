import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/weight_log_entity.dart';
import '../../domain/repositories/weight_repository.dart';
import '../datasources/weights_api_datasource.dart';
import '../models/weight_models.dart';

final weightsApiDatasourceProvider = Provider<WeightsApiDatasource>((ref) {
  return WeightsApiDatasource(ref.read(apiClientProvider));
});

final weightRepositoryProvider = Provider<WeightRepository>((ref) {
  return WeightRepositoryImpl(ref.read(weightsApiDatasourceProvider));
});

class WeightRepositoryImpl implements WeightRepository {
  WeightRepositoryImpl(this._datasource);

  final WeightsApiDatasource _datasource;

  @override
  Future<WeightLogEntity> create(double weightKg, DateTime loggedAt) async {
    final root = await _datasource.create(weightKg: weightKg, loggedAt: loggedAt);
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return WeightLogModel.fromJson(data).toEntity();
  }

  @override
  Future<List<WeightLogEntity>> list() async {
    final root = await _datasource.list();
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    final items = (data['items'] as List<dynamic>? ?? const []).whereType<Map<String, dynamic>>();
    return items.map((x) => WeightLogModel.fromJson(x).toEntity()).toList();
  }
}
