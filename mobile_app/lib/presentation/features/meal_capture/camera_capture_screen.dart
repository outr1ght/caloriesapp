import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:go_router/go_router.dart';

class CameraCaptureScreen extends StatefulWidget {
  const CameraCaptureScreen({super.key});

  @override
  State<CameraCaptureScreen> createState() => _CameraCaptureScreenState();
}

class _CameraCaptureScreenState extends State<CameraCaptureScreen> {
  CameraController? _controller;

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    final cameras = await availableCameras();
    if (cameras.isEmpty) return;

    final ctrl = CameraController(cameras.first, ResolutionPreset.medium, enableAudio: false);
    await ctrl.initialize();
    if (!mounted) {
      await ctrl.dispose();
      return;
    }
    setState(() => _controller = ctrl);
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final ctrl = _controller;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.captureWithCameraAction)),
      body: ctrl == null || !ctrl.value.isInitialized ? const Center(child: CircularProgressIndicator()) : CameraPreview(ctrl),
      floatingActionButton: FloatingActionButton(
        onPressed: ctrl == null || !ctrl.value.isInitialized
            ? null
            : () async {
                final x = await ctrl.takePicture();
                if (!mounted) return;
                context.go('/meal-capture/preview', extra: x.path);
              },
        child: const Icon(Icons.camera),
      ),
    );
  }
}
