import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/report_repository_impl.dart';
import '../../domain/entities/nutrition_report_entity.dart';

final dashboardReportProvider = FutureProvider<NutritionReportEntity>((ref) async {
  final repository = ref.read(reportRepositoryProvider);
  return repository.getDaily();
});
