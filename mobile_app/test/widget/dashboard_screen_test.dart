import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/meals_provider.dart';
import 'package:calories_mobile/domain/entities/meal_entity.dart';
import 'package:calories_mobile/presentation/features/dashboard/dashboard_screen.dart';

class _LoadingMealsController extends MealsController {
  @override
  Future<List<MealEntity>> build() async {
    await Future<void>.delayed(const Duration(seconds: 5));
    return [];
  }
}

class _ErrorMealsController extends MealsController {
  @override
  Future<List<MealEntity>> build() async {
    throw Exception('failed');
  }
}

Widget _wrap(Widget child, List<Override> overrides) {
  return ProviderScope(
    overrides: overrides,
    child: MaterialApp(
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: child,
    ),
  );
}

void main() {
  testWidgets('dashboard shows loading state', (tester) async {
    await tester.pumpWidget(_wrap(const DashboardScreen(), [mealsProvider.overrideWith(_LoadingMealsController.new)]));
    expect(find.byType(CircularProgressIndicator), findsWidgets);
  });

  testWidgets('dashboard shows error state', (tester) async {
    await tester.pumpWidget(_wrap(const DashboardScreen(), [mealsProvider.overrideWith(_ErrorMealsController.new)]));
    await tester.pumpAndSettle();
    expect(find.textContaining('Unable'), findsWidgets);
  });
}
