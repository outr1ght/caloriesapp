import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../application/providers/meals_provider.dart';

class FoodDiaryScreen extends ConsumerWidget {
  const FoodDiaryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final mealsState = ref.watch(mealsProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.foodDiaryTitle)),
      body: RefreshIndicator(
        onRefresh: () => ref.read(mealsProvider.notifier).refresh(),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(l10n.todayLabel, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            if (mealsState.isLoading) const Center(child: CircularProgressIndicator()),
            if (mealsState.hasError) Text(l10n.genericLoadFailedLabel),
            if (mealsState.hasValue && mealsState.value!.isEmpty) Text(l10n.genericEmptyLabel),
            if (mealsState.hasValue)
              ...mealsState.value!.map(
                (meal) => Card(
                  child: ListTile(
                    title: Text(meal.title.isEmpty ? l10n.sampleMealTitle : meal.title),
                    subtitle: Text('${meal.calories.toStringAsFixed(0)} kcal'),
                    onTap: () => context.go('/food-diary/meal/${meal.id}'),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
