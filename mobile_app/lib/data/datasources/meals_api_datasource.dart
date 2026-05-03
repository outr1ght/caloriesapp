import '../api/generated/generated.dart';

class MealsApiDatasource {
  MealsApiDatasource(client) : _generated = GeneratedMealsApi(client);

  final GeneratedMealsApi _generated;

  Future<GeneratedMealListPage> list({int page = 1, int pageSize = 20}) {
    return _generated.listMeals(page: page, pageSize: pageSize);
  }

  Future<GeneratedMealRead> getById(String id) {
    return _generated.getMeal(id);
  }

  Future<GeneratedMealRead> update(String id, {required String title}) {
    return _generated.updateMeal(id, title: title);
  }

  Future<void> delete(String id) {
    return _generated.deleteMeal(id);
  }
}
