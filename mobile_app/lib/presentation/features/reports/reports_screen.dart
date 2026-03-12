import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../application/providers/reports_provider.dart';
import '../../../domain/entities/report_period.dart';

class ReportsScreen extends ConsumerWidget {
  const ReportsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final reportState = ref.watch(reportsProvider);
    final period = ref.watch(reportsPeriodProvider);

    int selected = 0;
    switch (period) {
      case ReportPeriod.daily:
        selected = 0;
        break;
      case ReportPeriod.weekly:
        selected = 1;
        break;
      case ReportPeriod.monthly:
        selected = 2;
        break;
    }

    return Scaffold(
      appBar: AppBar(title: Text(l10n.reportsTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          SegmentedButton<int>(
            segments: [
              ButtonSegment(value: 0, label: Text(l10n.dailyReportTab)),
              ButtonSegment(value: 1, label: Text(l10n.weeklyReportTab)),
              ButtonSegment(value: 2, label: Text(l10n.monthlyReportTab)),
            ],
            selected: {selected},
            onSelectionChanged: (value) {
              final next = value.first;
              final target = next == 0
                  ? ReportPeriod.daily
                  : next == 1
                  ? ReportPeriod.weekly
                  : ReportPeriod.monthly;
              ref.read(reportsProvider.notifier).setPeriod(target);
            },
          ),
          const SizedBox(height: 16),
          if (reportState.isLoading) const Center(child: CircularProgressIndicator()),
          if (reportState.hasError) ...[
            Text(l10n.genericLoadFailedLabel),
            const SizedBox(height: 8),
            OutlinedButton(
              onPressed: () => ref.read(reportsProvider.notifier).setPeriod(period),
              child: Text(l10n.retryAction),
            ),
          ],
          if (reportState.hasValue)
            Card(
              child: ListTile(
                title: Text(l10n.summaryCardsTitle),
                subtitle: Text('${reportState.value!.averageCalories.toStringAsFixed(0)} kcal'),
              ),
            ),
          const SizedBox(height: 12),
          if (reportState.hasValue)
            SizedBox(
              height: 220,
              child: LineChart(
                LineChartData(
                  lineBarsData: [
                    LineChartBarData(
                      spots: reportState.value!.trend
                          .asMap()
                          .entries
                          .map((e) => FlSpot(e.key.toDouble(), e.value.calories))
                          .toList(),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
