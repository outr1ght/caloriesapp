import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../application/providers/goals_provider.dart';
import '../../../application/providers/profile_provider.dart';
import '../../../core/utils/tdee_calculator.dart';
import '../../../domain/entities/goal_entity.dart';

class GoalSetupScreen extends ConsumerStatefulWidget {
  const GoalSetupScreen({super.key});

  @override
  ConsumerState<GoalSetupScreen> createState() => _GoalSetupScreenState();
}

class _GoalSetupScreenState extends ConsumerState<GoalSetupScreen> {
  final _calorieController = TextEditingController();
  final _proteinController = TextEditingController(text: '120');
  final _carbsController = TextEditingController(text: '200');
  final _fatController = TextEditingController(text: '70');

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final goal = ref.read(goalsProvider).valueOrNull;
      if (goal != null) {
        _calorieController.text = goal.targetCalories.toString();
        _proteinController.text = goal.targetProtein.toString();
        _carbsController.text = goal.targetCarbs.toString();
        _fatController.text = goal.targetFat.toString();
      } else {
        final p = ref.read(profileProvider).valueOrNull;
        if (p != null) {
          final tdee = TdeeCalculator.estimate(
            age: p.age,
            heightCm: p.heightCm,
            weightKg: p.weightKg,
            gender: p.gender,
            activityLevel: p.activityLevel,
          );
          _calorieController.text = tdee.toString();
        } else {
          _calorieController.text = '2200';
        }
      }
      setState(() {});
    });
  }

  @override
  void dispose() {
    _calorieController.dispose();
    _proteinController.dispose();
    _carbsController.dispose();
    _fatController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final goalsState = ref.watch(goalsProvider);
    final profile = ref.watch(profileProvider).valueOrNull;

    final tdee = profile == null
        ? 2200
        : TdeeCalculator.estimate(
            age: profile.age,
            heightCm: profile.heightCm,
            weightKg: profile.weightKg,
            gender: profile.gender,
            activityLevel: profile.activityLevel,
          );

    return Scaffold(
      appBar: AppBar(title: Text(l10n.goalSetupTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(child: ListTile(title: Text(l10n.tdeeLabel), subtitle: Text('$tdee kcal'))),
          const SizedBox(height: 12),
          TextField(
            controller: _calorieController,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText: l10n.calorieGoalLabel),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _proteinController,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText: l10n.proteinTargetLabel),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _carbsController,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText: l10n.carbsTargetLabel),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _fatController,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText: l10n.fatTargetLabel),
          ),
          const SizedBox(height: 16),
          if (goalsState.hasError) Text(l10n.genericSaveFailedLabel),
          FilledButton(
            onPressed: goalsState.isLoading ? null : () => _save(context, ref, profile?.activityLevel ?? 'moderate'),
            child: Text(l10n.saveGoalAction),
          ),
        ],
      ),
    );
  }

  Future<void> _save(BuildContext context, WidgetRef ref, String activityLevel) async {
    final l10n = AppLocalizations.of(context)!;
    final calories = int.tryParse(_calorieController.text.trim()) ?? 0;
    final protein = int.tryParse(_proteinController.text.trim()) ?? 0;
    final carbs = int.tryParse(_carbsController.text.trim()) ?? 0;
    final fat = int.tryParse(_fatController.text.trim()) ?? 0;

    if (calories <= 0 || protein < 0 || carbs < 0 || fat < 0) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.goalValidationMessage)));
      return;
    }

    final goal = GoalEntity(
      id: '',
      activityLevel: activityLevel,
      strategy: 'maintain',
      targetCalories: calories,
      targetProtein: protein,
      targetCarbs: carbs,
      targetFat: fat,
    );

    await ref.read(goalsProvider.notifier).save(goal);
    if (mounted && !ref.read(goalsProvider).hasError) {
      context.go('/dashboard');
    }
  }
}
