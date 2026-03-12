import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../meals/application/meals_controller.dart';

class AnalysisScreen extends ConsumerWidget {
  const AnalysisScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    const confidence = 0.62;
    const requiresManualReview = confidence < 0.65;
    final mealsState = ref.watch(mealsControllerProvider);

    final sampleItems = <Map<String, String>>[
      {'name': l10n.analysisItemChicken, 'amount': '160 g'},
      {'name': l10n.analysisItemRice, 'amount': '120 g'},
      {'name': l10n.analysisItemBroccoli, 'amount': '80 g'},
    ];

    return Scaffold(
      appBar: AppBar(title: Text(l10n.mealAnalysisTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(l10n.confidenceValue(confidence.toStringAsFixed(2))),
          if (requiresManualReview)
            Card(
              color: Theme.of(context).colorScheme.errorContainer,
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Text(l10n.manualReviewRequired),
              ),
            ),
          const SizedBox(height: 12),
          ...sampleItems.map(
            (item) => Card(
              child: ListTile(
                title: Text(item['name'] ?? ''),
                trailing: Text(item['amount'] ?? ''),
              ),
            ),
          ),
          const SizedBox(height: 8),
          OutlinedButton(onPressed: () {}, child: Text(l10n.editIngredientsAction)),
          const SizedBox(height: 16),
          Text(l10n.disclaimerApprox),
          if (mealsState.hasError)
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: Text(
                l10n.saveMealFailedMessage,
                style: TextStyle(color: Theme.of(context).colorScheme.error),
              ),
            ),
        ],
      ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16),
        child: FilledButton(
          onPressed: () async {
            await ref.read(mealsControllerProvider.notifier).saveDemoMeal();
            if (context.mounted) context.go('/diary');
          },
          child: Text(l10n.saveMealAction),
        ),
      ),
    );
  }
}
