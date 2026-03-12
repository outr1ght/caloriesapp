import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../meals/application/meals_controller.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final mealsState = ref.watch(mealsControllerProvider);

    final totalCalories = mealsState.valueOrNull?.fold<double>(0, (sum, m) => sum + m.nutrition.calories) ?? 0;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.todayTitle)),
      body: RefreshIndicator(
        onRefresh: () => ref.read(mealsControllerProvider.notifier).refreshMeals(),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Card(
              child: ListTile(
                title: Text(l10n.caloriesLabel),
                subtitle: Text('${totalCalories.toStringAsFixed(0)} / 2000'),
              ),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              children: [
                FilledButton(onPressed: () => context.go('/capture'), child: Text(l10n.logMealAction)),
                OutlinedButton(onPressed: () => context.go('/reports'), child: Text(l10n.reportsNav)),
                OutlinedButton(onPressed: () => context.go('/barcode'), child: Text(l10n.scanBarcodeAction)),
              ],
            ),
            const SizedBox(height: 16),
            Text(l10n.recentMealsLabel, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            if (mealsState.isLoading) const Center(child: CircularProgressIndicator()),
            if (mealsState.hasError) Text(l10n.loadMealsError),
            if (mealsState.hasValue && (mealsState.value?.isEmpty ?? true)) Text(l10n.emptyMealsLabel),
            if (mealsState.hasValue)
              ...mealsState.value!.take(5).map(
                (meal) => Card(
                  child: ListTile(
                    title: Text(meal.mealType),
                    subtitle: Text('${meal.nutrition.calories.toStringAsFixed(0)} kcal'),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
