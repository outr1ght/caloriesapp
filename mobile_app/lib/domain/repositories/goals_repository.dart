import '../entities/goal_entity.dart';

abstract class GoalsRepository {
  Future<GoalEntity?> getActiveGoal();
  Future<GoalEntity> saveGoal(GoalEntity goal);
  Future<bool> hasActiveGoal();
}
