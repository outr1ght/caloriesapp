import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client_provider.dart';
import '../../domain/entities/meal_entity.dart';
import '../../domain/repositories/meal_repository.dart';
import '../datasources/meals_api_datasource.dart';
import '../models/meal_models.dart';

final mealsApiDatasourceProvider = Provider<MealsApiDatasource>((ref) {
  return MealsApiDatasource(ref.read(apiClientProvider));
});

final mealRepositoryProvider = Provider<MealRepository>((ref) {
  return MealRepositoryImpl(ref.read(mealsApiDatasourceProvider));
});

class MealRepositoryImpl implements MealRepository {
  MealRepositoryImpl(this._datasource);

  final MealsApiDatasource _datasource;

  @override
  Future<MealEntity> getById(String id) async {
    final root = await _datasource.getById(id);
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    return MealModel.fromJson(data).toEntity();
  }

  @override
  Future<List<MealEntity>> list({int page = 1, int pageSize = 20}) async {
    final root = await _datasource.list(page: page, pageSize: pageSize);
    final data = (root['data'] as Map<String, dynamic>?) ?? root;
    final items = (data['items'] as List<dynamic>? ?? const []).whereType<Map<String, dynamic>>();
    return items.map((x) => MealModel.fromJson(x).toEntity()).toList();
  }
}
