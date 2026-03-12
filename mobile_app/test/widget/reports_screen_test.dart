import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/application/providers/reports_provider.dart';
import 'package:calories_mobile/domain/entities/nutrition_report_entity.dart';
import 'package:calories_mobile/presentation/features/reports/reports_screen.dart';

class _LoadingReportsController extends ReportsController {
  @override
  Future<NutritionReportEntity> build() async {
    await Future<void>.delayed(const Duration(seconds: 5));
    return const NutritionReportEntity(
      totalCalories: 0,
      averageCalories: 0,
      protein: 0,
      carbs: 0,
      fat: 0,
      trend: [],
    );
  }
}

class _ErrorReportsController extends ReportsController {
  @override
  Future<NutritionReportEntity> build() async {
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
  testWidgets('reports shows loading state', (tester) async {
    await tester.pumpWidget(_wrap(const ReportsScreen(), [reportsProvider.overrideWith(_LoadingReportsController.new)]));
    expect(find.byType(CircularProgressIndicator), findsWidgets);
  });

  testWidgets('reports shows error state', (tester) async {
    await tester.pumpWidget(_wrap(const ReportsScreen(), [reportsProvider.overrideWith(_ErrorReportsController.new)]));
    await tester.pumpAndSettle();
    expect(find.textContaining('Unable'), findsWidgets);
  });
}
