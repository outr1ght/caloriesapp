import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../application/providers/meal_planner_provider.dart';

class MealPlannerScreen extends ConsumerWidget {
  const MealPlannerScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final state = ref.watch(mealPlannerProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.mealPlannerTitle)),
      body: RefreshIndicator(
        onRefresh: () => ref.read(mealPlannerProvider.notifier).refresh(),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (state.isLoading) const Center(child: CircularProgressIndicator()),
            if (state.hasError) Text(l10n.genericLoadFailedLabel),
            if (state.hasValue && state.value!.isEmpty) Text(l10n.genericEmptyLabel),
            if (state.hasValue)
              ...state.value!.map(
                (plan) => Card(
                  child: ListTile(
                    title: Text(plan.title.isEmpty ? l10n.mealPlannerWeekLabel : plan.title),
                    subtitle: Text(plan.planDate.toLocal().toIso8601String().split('T').first),
                    trailing: Text(plan.status),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
