import 'package:flutter/material.dart';
import 'package:calories_mobile/l10n/generated/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../application/providers/meal_detail_provider.dart';
import '../../../application/providers/meals_provider.dart';
import '../../../data/repositories/meal_repository_impl.dart';

class MealDetailScreen extends ConsumerStatefulWidget {
  const MealDetailScreen({super.key, required this.mealId});

  final String mealId;

  @override
  ConsumerState<MealDetailScreen> createState() => _MealDetailScreenState();
}

class _MealDetailScreenState extends ConsumerState<MealDetailScreen> {
  final _titleController = TextEditingController();
  bool _initialized = false;
  bool _saving = false;
  bool _deleting = false;

  @override
  void dispose() {
    _titleController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final mealState = ref.watch(mealDetailProvider(widget.mealId));
    final meal = mealState.valueOrNull;

    if (!_initialized && meal != null) {
      _titleController.text = meal.title;
      _initialized = true;
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.mealDetailTitle),
        actions: [
          IconButton(
            onPressed: meal == null || _deleting ? null : () => _delete(context),
            icon: _deleting ? const SizedBox.square(dimension: 18, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.delete_outline),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (mealState.isLoading) const Center(child: CircularProgressIndicator()),
          if (mealState.hasError) Text(l10n.genericLoadFailedLabel),
          if (meal != null) ...[
            Card(child: ListTile(title: Text(l10n.mealIdLabel), subtitle: Text(meal.id))),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: TextField(
                  controller: _titleController,
                  decoration: InputDecoration(labelText: l10n.dishNameLabel),
                ),
              ),
            ),
            Card(child: ListTile(title: Text(l10n.calorieGoalLabel), subtitle: Text('${meal.calories.toStringAsFixed(0)} kcal'))),
            const SizedBox(height: 12),
            if (_saving) const LinearProgressIndicator(),
            FilledButton(
              onPressed: _saving ? null : () => _save(context),
              child: Text(l10n.saveMealAction),
            ),
          ],
        ],
      ),
    );
  }

  Future<void> _save(BuildContext context) async {
    final l10n = AppLocalizations.of(context)!;
    final title = _titleController.text.trim();
    if (title.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.genericSaveFailedLabel)));
      return;
    }

    setState(() => _saving = true);
    try {
      await ref.read(mealRepositoryProvider).updateTitle(widget.mealId, title);
      ref.invalidate(mealDetailProvider(widget.mealId));
      await ref.read(mealsProvider.notifier).refresh();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.saveSuccessMessage)));
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.genericSaveFailedLabel)));
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  Future<void> _delete(BuildContext context) async {
    final l10n = AppLocalizations.of(context)!;
    setState(() => _deleting = true);
    try {
      await ref.read(mealRepositoryProvider).delete(widget.mealId);
      await ref.read(mealsProvider.notifier).refresh();
      if (!mounted) return;
      context.go('/food-diary');
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.genericSaveFailedLabel)));
    } finally {
      if (mounted) setState(() => _deleting = false);
    }
  }
}

