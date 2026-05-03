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
    final meal = await _datasource.getById(id);
    return MealModel.fromGenerated(meal).toEntity();
  }

  @override
  Future<List<MealEntity>> list({int page = 1, int pageSize = 20}) async {
    final pageResponse = await _datasource.list(page: page, pageSize: pageSize);
    return pageResponse.items.map((x) => MealModel.fromGenerated(x).toEntity()).toList();
  }

  @override
  Future<MealEntity> updateTitle(String id, String title) async {
    final meal = await _datasource.update(id, title: title);
    return MealModel.fromGenerated(meal).toEntity();
  }

  @override
  Future<void> delete(String id) {
    return _datasource.delete(id);
  }
}
