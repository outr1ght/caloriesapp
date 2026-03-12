import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../application/providers/meal_capture_provider.dart';

class PhotoPreviewScreen extends ConsumerWidget {
  const PhotoPreviewScreen({super.key, required this.path});

  final String path;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final captureState = ref.watch(mealCaptureProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.photoPreviewTitle)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Expanded(child: ClipRRect(borderRadius: BorderRadius.circular(16), child: Image.file(File(path), fit: BoxFit.cover))),
            const SizedBox(height: 12),
            if (captureState.hasError) Text(l10n.genericSaveFailedLabel),
            if (captureState.isLoading) const LinearProgressIndicator(),
            Row(
              children: [
                Expanded(child: OutlinedButton(onPressed: () => context.go('/meal-capture'), child: Text(l10n.retakeAction))),
                const SizedBox(width: 8),
                Expanded(
                  child: FilledButton(
                    onPressed: captureState.isLoading
                        ? null
                        : () async {
                            await ref.read(mealCaptureProvider.notifier).upload(path);
                            final uploaded = ref.read(mealCaptureProvider).valueOrNull;
                            if (uploaded == null || !context.mounted) return;
                            context.go('/meal-analysis', extra: uploaded.imageId);
                          },
                    child: Text(l10n.analyzeMealAction),
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
