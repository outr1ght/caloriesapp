import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../application/providers/profile_provider.dart';
import '../../../domain/entities/profile_entity.dart';

class ProfileSetupScreen extends ConsumerStatefulWidget {
  const ProfileSetupScreen({super.key});

  @override
  ConsumerState<ProfileSetupScreen> createState() => _ProfileSetupScreenState();
}

class _ProfileSetupScreenState extends ConsumerState<ProfileSetupScreen> {
  final _firstName = TextEditingController();
  final _lastName = TextEditingController();
  final _age = TextEditingController();
  final _height = TextEditingController();
  final _weight = TextEditingController();
  String _gender = 'male';
  String _activity = 'moderate';

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final existing = ref.read(profileProvider).valueOrNull;
      if (existing == null) return;
      _firstName.text = existing.firstName;
      _lastName.text = existing.lastName;
      _age.text = existing.age > 0 ? existing.age.toString() : '';
      _height.text = existing.heightCm > 0 ? existing.heightCm.toStringAsFixed(0) : '';
      _weight.text = existing.weightKg > 0 ? existing.weightKg.toStringAsFixed(1) : '';
      _gender = existing.gender;
      _activity = existing.activityLevel;
      setState(() {});
    });
  }

  @override
  void dispose() {
    _firstName.dispose();
    _lastName.dispose();
    _age.dispose();
    _height.dispose();
    _weight.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final profileState = ref.watch(profileProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.profileSetupTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (profileState.isLoading) const LinearProgressIndicator(),
          TextField(controller: _firstName, decoration: InputDecoration(labelText: l10n.firstNameLabel)),
          const SizedBox(height: 12),
          TextField(controller: _lastName, decoration: InputDecoration(labelText: l10n.lastNameLabel)),
          const SizedBox(height: 12),
          TextField(controller: _age, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.ageLabel)),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            value: _gender,
            decoration: InputDecoration(labelText: l10n.genderLabel),
            items: [
              DropdownMenuItem(value: 'male', child: Text(l10n.genderMale)),
              DropdownMenuItem(value: 'female', child: Text(l10n.genderFemale)),
              DropdownMenuItem(value: 'other', child: Text(l10n.genderOther)),
            ],
            onChanged: (v) => setState(() => _gender = v ?? 'male'),
          ),
          const SizedBox(height: 12),
          TextField(controller: _height, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.heightLabel)),
          const SizedBox(height: 12),
          TextField(controller: _weight, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: l10n.weightLabel)),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            value: _activity,
            decoration: InputDecoration(labelText: l10n.activityLevelLabel),
            items: [
              DropdownMenuItem(value: 'sedentary', child: Text(l10n.activitySedentary)),
              DropdownMenuItem(value: 'light', child: Text(l10n.activityLight)),
              DropdownMenuItem(value: 'moderate', child: Text(l10n.activityModerate)),
              DropdownMenuItem(value: 'active', child: Text(l10n.activityActive)),
            ],
            onChanged: (v) => setState(() => _activity = v ?? 'moderate'),
          ),
          const SizedBox(height: 16),
          if (profileState.hasError) Text(l10n.genericSaveFailedLabel),
          FilledButton(
            onPressed: profileState.isLoading ? null : () => _submit(context, ref),
            child: Text(l10n.continueAction),
          ),
        ],
      ),
    );
  }

  Future<void> _submit(BuildContext context, WidgetRef ref) async {
    final l10n = AppLocalizations.of(context)!;
    final first = _firstName.text.trim();
    final age = int.tryParse(_age.text.trim()) ?? 0;
    final height = double.tryParse(_height.text.trim()) ?? 0;
    final weight = double.tryParse(_weight.text.trim()) ?? 0;

    if (first.isEmpty || age < 10 || height <= 0 || weight <= 0) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(l10n.profileValidationMessage)));
      return;
    }

    final entity = ProfileEntity(
      firstName: first,
      lastName: _lastName.text.trim(),
      age: age,
      gender: _gender,
      heightCm: height,
      weightKg: weight,
      activityLevel: _activity,
    );

    await ref.read(profileProvider.notifier).save(entity);
    if (mounted && !ref.read(profileProvider).hasError) {
      context.go('/goal-setup');
    }
  }
}
