import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../application/goal_setup_controller.dart';
import '../domain/calorie_goal.dart';

class CalorieGoalSetupScreen extends ConsumerStatefulWidget {
  const CalorieGoalSetupScreen({super.key});

  @override
  ConsumerState<CalorieGoalSetupScreen> createState() => _CalorieGoalSetupScreenState();
}

class _CalorieGoalSetupScreenState extends ConsumerState<CalorieGoalSetupScreen> {
  final _caloriesController = TextEditingController(text: '2000');
  final _proteinController = TextEditingController(text: '120');
  final _carbsController = TextEditingController(text: '200');
  final _fatController = TextEditingController(text: '70');

  @override
  void dispose() {
    _caloriesController.dispose();
    _proteinController.dispose();
    _carbsController.dispose();
    _fatController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.goalSetupTitle)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: _caloriesController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.goalCaloriesLabel)),
            const SizedBox(height: 12),
            TextField(controller: _proteinController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.goalProteinLabel)),
            const SizedBox(height: 12),
            TextField(controller: _carbsController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.goalCarbsLabel)),
            const SizedBox(height: 12),
            TextField(controller: _fatController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.goalFatLabel)),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: () async {
                  final goal = CalorieGoal(
                    dailyCalories: int.tryParse(_caloriesController.text.trim()) ?? 2000,
                    proteinGrams: int.tryParse(_proteinController.text.trim()) ?? 120,
                    carbsGrams: int.tryParse(_carbsController.text.trim()) ?? 200,
                    fatGrams: int.tryParse(_fatController.text.trim()) ?? 70,
                  );
                  await ref.read(goalSetupControllerProvider.notifier).save(goal);
                  if (context.mounted) context.go('/dashboard');
                },
                child: Text(l10n.saveMealAction),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
