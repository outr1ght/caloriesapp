import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../application/reports_controller.dart';

class ReportsScreen extends ConsumerWidget {
  const ReportsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final reportState = ref.watch(reportsControllerProvider);

    final calories = reportState.valueOrNull?.calories ?? 0;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.reportsNav)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(l10n.weeklyCaloriesTrendLabel, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            SizedBox(
              height: 220,
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: reportState.isLoading
                      ? const Center(child: CircularProgressIndicator())
                      : LineChart(
                          LineChartData(
                            minY: 1200,
                            maxY: 2600,
                            gridData: const FlGridData(show: true),
                            titlesData: const FlTitlesData(show: true),
                            lineBarsData: [
                              LineChartBarData(
                                spots: [
                                  FlSpot(1, (calories * 0.90).clamp(1200, 2600).toDouble()),
                                  FlSpot(2, (calories * 1.00).clamp(1200, 2600).toDouble()),
                                  FlSpot(3, (calories * 0.95).clamp(1200, 2600).toDouble()),
                                ],
                              ),
                            ],
                          ),
                        ),
                ),
              ),
            ),
            const SizedBox(height: 8),
            Text(l10n.chartReadableHint),
            const SizedBox(height: 12),
            if (reportState.hasError) Text(l10n.loadReportsError),
            if (reportState.hasValue)
              Card(
                child: ListTile(
                  title: Text(l10n.caloriesLabel),
                  subtitle: Text('${reportState.value!.calories.toStringAsFixed(0)} kcal'),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
