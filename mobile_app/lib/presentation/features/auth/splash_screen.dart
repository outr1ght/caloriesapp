import 'package:flutter/material.dart';
import 'package:calories_mobile/l10n/generated/app_localizations.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    return Scaffold(body: Center(child: Text(l10n.loadingLabel)));
  }
}

