import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/barcode_repository_impl.dart';
import '../../domain/entities/barcode_lookup_entity.dart';
import '../usecases/lookup_barcode_usecase.dart';
import '../usecases/save_barcode_meal_usecase.dart';

final barcodeProvider = AsyncNotifierProvider<BarcodeController, BarcodeLookupEntity?>(BarcodeController.new);

class BarcodeController extends AsyncNotifier<BarcodeLookupEntity?> {
  @override
  Future<BarcodeLookupEntity?> build() async {
    return null;
  }

  Future<void> lookup(String code) async {
    final trimmed = code.trim();
    if (trimmed.length < 4) {
      state = const AsyncData(BarcodeLookupEntity(found: false));
      return;
    }

    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = LookupBarcodeUseCase(ref.read(barcodeRepositoryProvider));
      return usecase(trimmed);
    });
  }

  Future<String?> saveAsMeal() async {
    final current = state.valueOrNull;
    final product = current?.product;
    if (product == null) return null;

    final usecase = SaveBarcodeMealUseCase(ref.read(barcodeRepositoryProvider));
    return usecase(product);
  }
}
