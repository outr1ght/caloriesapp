import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/i18n/locale_controller.dart';
import '../../auth/application/auth_controller.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final locale = ref.watch(localeControllerProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.settingsNav)),
      body: ListView(
        children: [
          ListTile(
            title: Text(l10n.languageLabel),
            subtitle: Text(locale?.languageCode ?? l10n.systemLabel),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _pickLanguage(context, ref),
          ),
          ListTile(
            title: Text(l10n.unitSystemLabel),
            subtitle: Text(l10n.unitSystemValue),
          ),
          ListTile(
            title: Text(l10n.disclaimerLabel),
            subtitle: Text(l10n.notMedicalDisclaimer),
          ),
          const SizedBox(height: 24),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: OutlinedButton(
              onPressed: () async {
                await ref.read(authControllerProvider.notifier).logout();
                if (context.mounted) {
                  context.go('/login');
                }
              },
              child: Text(l10n.logoutAction),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _pickLanguage(BuildContext context, WidgetRef ref) async {
    final l10n = AppLocalizations.of(context)!;

    final chosen = await showDialog<String?>(
      context: context,
      builder: (context) => SimpleDialog(
        title: Text(l10n.chooseLanguageTitle),
        children: [
          SimpleDialogOption(
            onPressed: () => Navigator.pop(context, null),
            child: Text(l10n.systemDefaultLanguage),
          ),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'en'), child: Text(l10n.languageEnglish)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'es'), child: Text(l10n.languageSpanish)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'de'), child: Text(l10n.languageGerman)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'fr'), child: Text(l10n.languageFrench)),
          SimpleDialogOption(onPressed: () => Navigator.pop(context, 'ru'), child: Text(l10n.languageRussian)),
        ],
      ),
    );

    await ref.read(localeControllerProvider.notifier).setLocale(chosen);
  }
}
