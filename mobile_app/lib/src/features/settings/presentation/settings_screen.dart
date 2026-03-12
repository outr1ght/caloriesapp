import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/i18n/locale_controller.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.settingsNav)),
      body: ListView(
        children: [
          ListTile(
            title: Text(l10n.languageLabel),
            subtitle: Text(l10n.languageListLabel),
            onTap: () => ref.read(localeControllerProvider.notifier).setLocale('en'),
          ),
          ListTile(
            title: Text(l10n.unitSystemLabel),
            subtitle: Text(l10n.unitSystemValue),
          ),
          ListTile(
            title: Text(l10n.disclaimerLabel),
            subtitle: Text(l10n.notMedicalDisclaimer),
          ),
        ],
      ),
    );
  }
}
