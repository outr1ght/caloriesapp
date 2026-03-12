import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:go_router/go_router.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final _controller = PageController();
  int _index = 0;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final pages = [
      (l10n.onboardingIntroTitle, l10n.onboardingIntroBody),
      (l10n.onboardingAssistantTitle, l10n.onboardingAssistantBody),
      (l10n.onboardingCameraTitle, l10n.onboardingCameraBody),
    ];

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Expanded(
              child: PageView.builder(
                controller: _controller,
                onPageChanged: (value) => setState(() => _index = value),
                itemCount: pages.length,
                itemBuilder: (context, i) => Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(pages[i].$1, style: Theme.of(context).textTheme.headlineMedium),
                    const SizedBox(height: 12),
                    Text(pages[i].$2),
                  ],
                ),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('${_index + 1}/${pages.length}'),
                FilledButton(
                  onPressed: () {
                    if (_index < pages.length - 1) {
                      _controller.nextPage(duration: const Duration(milliseconds: 220), curve: Curves.easeOut);
                    } else {
                      context.go('/login');
                    }
                  },
                  child: Text(_index < pages.length - 1 ? l10n.nextAction : l10n.getStartedAction),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
