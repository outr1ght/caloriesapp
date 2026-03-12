import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';

class MealCaptureScreen extends StatefulWidget {
  const MealCaptureScreen({super.key});

  @override
  State<MealCaptureScreen> createState() => _MealCaptureScreenState();
}

class _MealCaptureScreenState extends State<MealCaptureScreen> {
  final ImagePicker _picker = ImagePicker();

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.mealCaptureTitle)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            FilledButton.icon(
              onPressed: () => context.go('/meal-capture/camera'),
              icon: const Icon(Icons.camera_alt_outlined),
              label: Text(l10n.captureWithCameraAction),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () async {
                final x = await _picker.pickImage(source: ImageSource.gallery, imageQuality: 90);
                if (x == null || !mounted) return;
                if (!File(x.path).existsSync()) return;
                context.go('/meal-capture/preview', extra: x.path);
              },
              icon: const Icon(Icons.photo_library_outlined),
              label: Text(l10n.pickFromGalleryAction),
            )
          ],
        ),
      ),
    );
  }
}
