import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

import '../../../application/providers/barcode_provider.dart';

class BarcodeScanScreen extends ConsumerStatefulWidget {
  const BarcodeScanScreen({super.key});

  @override
  ConsumerState<BarcodeScanScreen> createState() => _BarcodeScanScreenState();
}

class _BarcodeScanScreenState extends ConsumerState<BarcodeScanScreen> {
  final _manualController = TextEditingController();
  String? _code;
  bool _locked = false;

  @override
  void dispose() {
    _manualController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final state = ref.watch(barcodeProvider);
    final result = state.valueOrNull;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.barcodeScanTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          SizedBox(
            height: 220,
            child: MobileScanner(
              onDetect: (capture) async {
                if (_locked || capture.barcodes.isEmpty) return;
                final value = capture.barcodes.first.rawValue;
                if (value == null || value.isEmpty) return;
                _locked = true;
                setState(() => _code = value);
                _manualController.text = value;
                await ref.read(barcodeProvider.notifier).lookup(value);
                _locked = false;
              },
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _manualController,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText: l10n.barcodeScanTitle),
            onSubmitted: (value) => ref.read(barcodeProvider.notifier).lookup(value),
          ),
          const SizedBox(height: 8),
          FilledButton(
            onPressed: () => ref.read(barcodeProvider.notifier).lookup(_manualController.text),
            child: Text(l10n.nextAction),
          ),
          const SizedBox(height: 12),
          if (state.isLoading) const Center(child: CircularProgressIndicator()),
          if (state.hasError) Text(l10n.genericLoadFailedLabel),
          if (result != null && !result.found) Text(l10n.genericEmptyLabel),
          if (result?.product != null)
            Card(
              child: ListTile(
                title: Text(result!.product!.name),
                subtitle: Text(result.product!.brand.isEmpty ? '-' : result.product!.brand),
                trailing: Text(result.product!.barcode),
              ),
            ),
          if (result?.product != null)
            FilledButton(
              onPressed: () async {
                final mealId = await ref.read(barcodeProvider.notifier).saveAsMeal();
                if (!mounted || mealId == null || mealId.isEmpty) return;
                context.go('/food-diary/meal/$mealId');
              },
              child: Text(l10n.saveMealAction),
            ),
          const SizedBox(height: 8),
          Text(_code == null ? l10n.barcodeWaitingLabel : '${l10n.barcodeDetectedLabel}: $_code'),
        ],
      ),
    );
  }
}
