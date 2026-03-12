import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../application/providers/meal_analysis_provider.dart';

class MealAnalysisScreen extends ConsumerStatefulWidget {
  const MealAnalysisScreen({super.key, this.uploadedImageId});

  final String? uploadedImageId;

  @override
  ConsumerState<MealAnalysisScreen> createState() => _MealAnalysisScreenState();
}

class _MealAnalysisScreenState extends ConsumerState<MealAnalysisScreen> {
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final id = widget.uploadedImageId;
      if (id == null || id.isEmpty) return;
      ref.read(mealAnalysisProvider.notifier).analyze(id);
    });
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final state = ref.watch(mealAnalysisProvider);
    final analysis = state.valueOrNull;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.mealAnalysisTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (state.isLoading) const Center(child: CircularProgressIndicator()),
          if (state.hasError) ...[
            Text(l10n.genericLoadFailedLabel),
            const SizedBox(height: 8),
            OutlinedButton(
              onPressed: () {
                final id = widget.uploadedImageId;
                if (id == null || id.isEmpty) return;
                ref.read(mealAnalysisProvider.notifier).analyze(id);
              },
              child: Text(l10n.retryAction),
            ),
          ],
          if (analysis != null) ...[
            if (analysis.confidence < 0.6)
              Card(
                color: Theme.of(context).colorScheme.errorContainer,
                child: ListTile(
                  title: Text(l10n.lowConfidenceTitle),
                  subtitle: Text(l10n.lowConfidenceMessage),
                ),
              ),
            Card(child: ListTile(title: Text(l10n.dishNameLabel), subtitle: Text(analysis.items.isEmpty ? '-' : analysis.items.first.name))),
            Card(child: ListTile(title: Text(l10n.estimatedWeightLabel), subtitle: Text('${analysis.items.fold<double>(0, (s, x) => s + x.quantity).toStringAsFixed(0)} g'))),
            Card(child: ListTile(title: Text(l10n.confidenceLabel), subtitle: Text(analysis.confidence.toStringAsFixed(2)))),
            const SizedBox(height: 12),
            Text(l10n.ingredientsLabel, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            ...analysis.items.asMap().entries.map(
              (entry) => Card(
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      TextFormField(
                        initialValue: entry.value.name,
                        decoration: InputDecoration(labelText: l10n.ingredientsLabel),
                        onChanged: (value) => ref.read(mealAnalysisProvider.notifier).updateItemName(entry.key, value),
                      ),
                      const SizedBox(height: 6),
                      Text('${entry.value.quantity.toStringAsFixed(0)} ${entry.value.unit}'),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 12),
            if (_saving) const LinearProgressIndicator(),
            FilledButton(
              onPressed: _saving ? null : () => _save(context, ref),
              child: Text(l10n.saveMealAction),
            ),
          ],
        ],
      ),
    );
  }

  Future<void> _save(BuildContext context, WidgetRef ref) async {
    final l10n = AppLocalizations.of(context)!;

    if (ref.read(mealAnalysisProvider.notifier).hasInvalidItems()) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.invalidIngredientsMessage)));
      return;
    }

    setState(() => _saving = true);
    try {
      final mealId = await ref.read(mealAnalysisProvider.notifier).saveMeal();
      if (!mounted) return;
      if (mealId == null || mealId.isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.genericSaveFailedLabel)));
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.saveSuccessMessage)));
      context.go('/food-diary/meal/$mealId');
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.invalidIngredientsMessage)));
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }
}
