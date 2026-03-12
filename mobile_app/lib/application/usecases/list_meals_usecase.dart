import '../../domain/entities/meal_entity.dart';
import '../../domain/repositories/meal_repository.dart';

class ListMealsUseCase {
  const ListMealsUseCase(this._repository);

  final MealRepository _repository;

  Future<List<MealEntity>> call({int page = 1, int pageSize = 20}) {
    return _repository.list(page: page, pageSize: pageSize);
  }
}
