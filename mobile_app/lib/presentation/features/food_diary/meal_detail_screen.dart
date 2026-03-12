import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../application/providers/meal_detail_provider.dart';

class MealDetailScreen extends ConsumerWidget {
  const MealDetailScreen({super.key, required this.mealId});

  final String mealId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final mealState = ref.watch(mealDetailProvider(mealId));

    return Scaffold(
      appBar: AppBar(title: Text(l10n.mealDetailTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (mealState.isLoading) const Center(child: CircularProgressIndicator()),
          if (mealState.hasError) Text(l10n.genericLoadFailedLabel),
          if (mealState.hasValue) ...[
            Card(child: ListTile(title: Text(l10n.mealIdLabel), subtitle: Text(mealState.value!.id))),
            Card(child: ListTile(title: Text(l10n.dishNameLabel), subtitle: Text(mealState.value!.title))),
            Card(child: ListTile(title: Text(l10n.calorieGoalLabel), subtitle: Text('${mealState.value!.calories.toStringAsFixed(0)} kcal'))),
            const SizedBox(height: 12),
            FilledButton(onPressed: () {}, child: Text(l10n.editMealAction)),
          ],
        ],
      ),
    );
  }
}
