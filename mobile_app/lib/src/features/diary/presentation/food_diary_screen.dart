import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../meals/application/meals_controller.dart';

class FoodDiaryScreen extends ConsumerWidget {
  const FoodDiaryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final mealsState = ref.watch(mealsControllerProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.foodDiaryTitle)),
      body: RefreshIndicator(
        onRefresh: () => ref.read(mealsControllerProvider.notifier).refreshMeals(),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (mealsState.isLoading) const Center(child: CircularProgressIndicator()),
            if (mealsState.hasError) Text(l10n.loadMealsError),
            if (mealsState.hasValue && (mealsState.value?.isEmpty ?? true)) Text(l10n.emptyMealsLabel),
            if (mealsState.hasValue)
              ...mealsState.value!.map(
                (meal) => Card(
                  child: ListTile(
                    title: Text(meal.mealType),
                    subtitle: Text('${meal.nutrition.calories.toStringAsFixed(0)} kcal'),
                    trailing: Text('${meal.items.length}'),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
