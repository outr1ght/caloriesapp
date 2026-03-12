import '../../domain/entities/goal_entity.dart';
import '../../domain/repositories/goals_repository.dart';

class SaveGoalUseCase {
  const SaveGoalUseCase(this._repository);

  final GoalsRepository _repository;

  Future<GoalEntity> call(GoalEntity goal) {
    return _repository.saveGoal(goal);
  }
}
