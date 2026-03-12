import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../application/providers/weights_provider.dart';

class WeightTrackingScreen extends ConsumerStatefulWidget {
  const WeightTrackingScreen({super.key});

  @override
  ConsumerState<WeightTrackingScreen> createState() => _WeightTrackingScreenState();
}

class _WeightTrackingScreenState extends ConsumerState<WeightTrackingScreen> {
  final _weightController = TextEditingController();

  @override
  void dispose() {
    _weightController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final state = ref.watch(weightsProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.weightTrackingTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (state.hasValue && state.value!.isNotEmpty)
            Card(
              child: ListTile(
                title: Text(l10n.currentWeightLabel),
                subtitle: Text('${state.value!.first.weightKg.toStringAsFixed(1)} kg'),
              ),
            ),
          if (state.hasError) Text(l10n.genericLoadFailedLabel),
          if (state.isLoading) const Center(child: CircularProgressIndicator()),
          const SizedBox(height: 12),
          TextField(
            controller: _weightController,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText: l10n.weightLabel),
          ),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: () async {
              final value = double.tryParse(_weightController.text.trim());
              if (value == null || value <= 0) return;
              await ref.read(weightsProvider.notifier).addWeight(value);
              _weightController.clear();
            },
            child: Text(l10n.logWeightAction),
          ),
          const SizedBox(height: 12),
          if (state.hasValue)
            ...state.value!.map(
              (w) => ListTile(
                title: Text('${w.weightKg.toStringAsFixed(1)} kg'),
                subtitle: Text(w.loggedAt.toLocal().toIso8601String().split('T').first),
              ),
            ),
        ],
      ),
    );
  }
}
