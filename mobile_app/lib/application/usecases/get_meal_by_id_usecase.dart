import '../../domain/entities/meal_entity.dart';
import '../../domain/repositories/meal_repository.dart';

class GetMealByIdUseCase {
  const GetMealByIdUseCase(this._repository);

  final MealRepository _repository;

  Future<MealEntity> call(String id) {
    return _repository.getById(id);
  }
}
