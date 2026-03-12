import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/goals_provider.dart';
import 'package:calories_mobile/application/providers/profile_provider.dart';
import 'package:calories_mobile/domain/entities/goal_entity.dart';
import 'package:calories_mobile/domain/entities/profile_entity.dart';
import 'package:calories_mobile/presentation/features/goals/goal_setup_screen.dart';

class _GoalsIdleController extends GoalsController {
  @override
  Future<GoalEntity?> build() async => null;
}

class _ProfileReadyController extends ProfileController {
  @override
  Future<ProfileEntity?> build() async => const ProfileEntity(
    firstName: 'John',
    lastName: 'Doe',
    age: 30,
    gender: 'male',
    heightCm: 180,
    weightKg: 80,
    activityLevel: 'moderate',
  );
}

void main() {
  testWidgets('goal setup validates invalid values', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          goalsProvider.overrideWith(_GoalsIdleController.new),
          profileProvider.overrideWith(_ProfileReadyController.new),
        ],
        child: MaterialApp(
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: AppLocalizations.supportedLocales,
          home: const GoalSetupScreen(),
        ),
      ),
    );

    await tester.enterText(find.byType(TextField).first, '0');
    await tester.tap(find.byType(FilledButton));
    await tester.pump();

    expect(find.byType(SnackBar), findsOneWidget);
  });
}
