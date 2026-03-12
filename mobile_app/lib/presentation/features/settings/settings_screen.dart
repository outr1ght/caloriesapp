import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../application/providers/auth_provider.dart';
import '../../../application/providers/locale_provider.dart';
import '../../../application/providers/settings_provider.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final settingsState = ref.watch(settingsProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.settingsTitle)),
      body: ListView(
        children: [
          if (settingsState.isLoading) const LinearProgressIndicator(),
          if (settingsState.hasError)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Text(l10n.genericLoadFailedLabel),
            ),
          ListTile(
            title: Text(l10n.languageLabel),
            subtitle: Text(_languageLabel(l10n, settingsState.valueOrNull?.language)),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _pickLanguage(context, ref),
          ),
          ListTile(
            title: Text(l10n.unitSystemLabel),
            subtitle: Text(settingsState.valueOrNull?.unitSystem ?? 'metric'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _pickUnitSystem(context, ref),
          ),
          ListTile(
            title: Text(l10n.calorieGoalChangeLabel),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => context.go('/goal-setup'),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: OutlinedButton(
              onPressed: () async {
                await ref.read(authStateProvider.notifier).logout();
                if (context.mounted) {
                  context.go('/login');
                }
              },
              child: Text(l10n.logoutAction),
            ),
          )
        ],
      ),
    );
  }

  String _languageLabel(AppLocalizations l10n, String? code) {
    switch (code) {
      case 'es':
        return l10n.languageSpanish;
      case 'de':
        return l10n.languageGerman;
      case 'fr':
        return l10n.languageFrench;
      case 'ru':
        return l10n.languageRussian;
      case 'en':
      default:
        return l10n.languageEnglish;
    }
  }

  Future<void> _pickLanguage(BuildContext context, WidgetRef ref) async {
    final l10n = AppLocalizations.of(context)!;
    final picked = await showDialog<String>(
      context: context,
      builder: (context) => SimpleDialog(
        title: Text(l10n.languageLabel),
        children: [
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'en'), child: Text(l10n.languageEnglish)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'es'), child: Text(l10n.languageSpanish)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'de'), child: Text(l10n.languageGerman)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'fr'), child: Text(l10n.languageFrench)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'ru'), child: Text(l10n.languageRussian)),
        ],
      ),
    );

    if (picked == null) return;
    await ref.read(localeProvider.notifier).setLocale(picked);
    await ref.read(settingsProvider.notifier).updateLanguage(picked);
  }

  Future<void> _pickUnitSystem(BuildContext context, WidgetRef ref) async {
    final l10n = AppLocalizations.of(context)!;
    final selected = await showDialog<String>(
      context: context,
      builder: (context) => SimpleDialog(
        title: Text(l10n.unitSystemLabel),
        children: [
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'metric'), child: Text(l10n.unitMetricLabel)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'imperial'), child: Text(l10n.unitImperialLabel)),
        ],
      ),
    );

    if (selected == null) return;
    await ref.read(settingsProvider.notifier).updateUnitSystem(selected);
  }
}
