import 'calorie_goal.dart';

abstract class CalorieGoalRepository {
  Future<CalorieGoal?> load();
  Future<void> save(CalorieGoal goal);
}
