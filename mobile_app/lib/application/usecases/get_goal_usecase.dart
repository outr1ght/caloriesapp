import '../../domain/entities/goal_entity.dart';
import '../../domain/repositories/goals_repository.dart';

class GetGoalUseCase {
  const GetGoalUseCase(this._repository);

  final GoalsRepository _repository;

  Future<GoalEntity?> call() {
    return _repository.getActiveGoal();
  }
}
