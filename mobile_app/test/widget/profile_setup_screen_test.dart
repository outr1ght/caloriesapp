import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/profile_provider.dart';
import 'package:calories_mobile/domain/entities/profile_entity.dart';
import 'package:calories_mobile/presentation/features/profile/profile_setup_screen.dart';

class _ProfileIdleController extends ProfileController {
  @override
  Future<ProfileEntity?> build() async => null;
}

void main() {
  testWidgets('profile setup validates empty form', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [profileProvider.overrideWith(_ProfileIdleController.new)],
        child: MaterialApp(
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: AppLocalizations.supportedLocales,
          home: const ProfileSetupScreen(),
        ),
      ),
    );

    await tester.tap(find.byType(FilledButton));
    await tester.pump();

    expect(find.byType(SnackBar), findsOneWidget);
  });
}
