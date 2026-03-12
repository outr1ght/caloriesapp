import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../application/providers/recommendations_provider.dart';

class RecommendationsScreen extends ConsumerWidget {
  const RecommendationsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final state = ref.watch(recommendationsProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.recommendationsTitle)),
      body: RefreshIndicator(
        onRefresh: () => ref.read(recommendationsProvider.notifier).refresh(),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (state.isLoading) const Center(child: CircularProgressIndicator()),
            if (state.hasError) Text(l10n.genericLoadFailedLabel),
            if (state.hasValue && state.value!.isEmpty) Text(l10n.genericEmptyLabel),
            if (state.hasValue)
              ...state.value!.map(
                (item) => Card(
                  child: ListTile(
                    title: Text(item.title.isEmpty ? l10n.recommendationCardTitle : item.title),
                    subtitle: Text(item.type),
                    trailing: PopupMenuButton<String>(
                      onSelected: (value) {
                        if (value == 'applied') {
                          ref.read(recommendationsProvider.notifier).markApplied(item.id);
                        } else if (value == 'dismissed') {
                          ref.read(recommendationsProvider.notifier).dismiss(item.id);
                        }
                      },
                      itemBuilder: (_) => [
                        PopupMenuItem(value: 'applied', child: Text(l10n.markAppliedAction)),
                        PopupMenuItem(value: 'dismissed', child: Text(l10n.dismissAction)),
                      ],
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
