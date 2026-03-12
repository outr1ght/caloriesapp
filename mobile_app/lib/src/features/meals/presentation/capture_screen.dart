import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:go_router/go_router.dart';

class CaptureScreen extends StatelessWidget {
  const CaptureScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.captureMealTitle)),
      body: Center(
        child: FilledButton(
          onPressed: () => context.go('/analysis'),
          child: Text(l10n.useDemoAnalysisAction),
        ),
      ),
    );
  }
}
