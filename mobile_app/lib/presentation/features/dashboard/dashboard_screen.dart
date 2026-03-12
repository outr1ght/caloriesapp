import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../application/providers/meals_provider.dart';
import '../../widgets/app_card.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final mealsState = ref.watch(mealsProvider);
    final totalCalories = mealsState.valueOrNull?.fold<double>(0, (sum, m) => sum + m.calories) ?? 0;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.dashboardTitle)),
      body: RefreshIndicator(
        onRefresh: () => ref.read(mealsProvider.notifier).refresh(),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            AppCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(l10n.dailyCaloriesProgressTitle),
                  const SizedBox(height: 8),
                  LinearProgressIndicator(value: (totalCalories / 2200).clamp(0, 1)),
                  const SizedBox(height: 8),
                  Text('${totalCalories.toStringAsFixed(0)} / 2200 kcal'),
                ],
              ),
            ),
            const SizedBox(height: 12),
            AppCard(child: ListTile(title: Text(l10n.macroSummaryTitle), subtitle: Text(l10n.macroSummarySample))),
            const SizedBox(height: 12),
            AppCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(l10n.recentMealsTitle),
                  const SizedBox(height: 8),
                  if (mealsState.hasError) ...[
                    Text(l10n.genericLoadFailedLabel),
                    const SizedBox(height: 8),
                    OutlinedButton(
                      onPressed: () => ref.read(mealsProvider.notifier).refresh(),
                      child: Text(l10n.retryAction),
                    ),
                  ],
                  if (mealsState.isLoading) const CircularProgressIndicator(),
                  if (mealsState.hasValue && mealsState.value!.isEmpty) Text(l10n.genericEmptyLabel),
                  if (mealsState.hasValue)
                    ...mealsState.value!.take(3).map((meal) => Text('${meal.title} - ${meal.calories.toStringAsFixed(0)} kcal')),
                ],
              ),
            ),
            const SizedBox(height: 12),
            FilledButton.icon(
              onPressed: () => context.go('/meal-capture'),
              icon: const Icon(Icons.add_a_photo_outlined),
              label: Text(l10n.quickAddMealAction),
            ),
          ],
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: 0,
        onDestinationSelected: (index) {
          switch (index) {
            case 0:
              context.go('/dashboard');
              break;
            case 1:
              context.go('/food-diary');
              break;
            case 2:
              context.go('/reports');
              break;
            case 3:
              context.go('/settings');
              break;
          }
        },
        destinations: [
          NavigationDestination(icon: const Icon(Icons.home_outlined), label: l10n.dashboardNav),
          NavigationDestination(icon: const Icon(Icons.restaurant_menu_outlined), label: l10n.diaryNav),
          NavigationDestination(icon: const Icon(Icons.bar_chart_outlined), label: l10n.reportsNav),
          NavigationDestination(icon: const Icon(Icons.settings_outlined), label: l10n.settingsNav),
        ],
      ),
    );
  }
}
