import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../application/profile_setup_controller.dart';
import '../domain/profile_setup.dart';

class ProfileSetupScreen extends ConsumerStatefulWidget {
  const ProfileSetupScreen({super.key});

  @override
  ConsumerState<ProfileSetupScreen> createState() => _ProfileSetupScreenState();
}

class _ProfileSetupScreenState extends ConsumerState<ProfileSetupScreen> {
  final _nameController = TextEditingController();
  final _ageController = TextEditingController();
  final _heightController = TextEditingController();
  final _weightController = TextEditingController();

  @override
  void dispose() {
    _nameController.dispose();
    _ageController.dispose();
    _heightController.dispose();
    _weightController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.profileSetupTitle)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: _nameController, decoration: InputDecoration(labelText: l10n.profileNameLabel)),
            const SizedBox(height: 12),
            TextField(controller: _ageController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.profileAgeLabel)),
            const SizedBox(height: 12),
            TextField(controller: _heightController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.profileHeightLabel)),
            const SizedBox(height: 12),
            TextField(controller: _weightController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.profileWeightLabel)),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: () async {
                  final profile = ProfileSetup(
                    name: _nameController.text.trim(),
                    age: int.tryParse(_ageController.text.trim()) ?? 0,
                    heightCm: double.tryParse(_heightController.text.trim()) ?? 0,
                    weightKg: double.tryParse(_weightController.text.trim()) ?? 0,
                  );
                  await ref.read(profileSetupControllerProvider.notifier).save(profile);
                  if (context.mounted) context.go('/goal-setup');
                },
                child: Text(l10n.continueAction),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
