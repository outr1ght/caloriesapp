import 'dart:io' show Platform;

import 'package:flutter_riverpod/flutter_riverpod.dart';

class AppConfig {
  const AppConfig({
    required this.apiBaseUrl,
    required this.connectTimeoutMs,
    required this.receiveTimeoutMs,
    required this.sendTimeoutMs,
  });

  final String apiBaseUrl;
  final int connectTimeoutMs;
  final int receiveTimeoutMs;
  final int sendTimeoutMs;
}

String _normalizeBaseUrl(String value) {
  final trimmed = value.trim();
  if (trimmed.isEmpty) return trimmed;
  return trimmed.endsWith('/') ? trimmed.substring(0, trimmed.length - 1) : trimmed;
}

String _resolveApiBaseUrl() {
  const override = String.fromEnvironment('API_BASE_URL', defaultValue: '');
  if (override.isNotEmpty) {
    return _normalizeBaseUrl(override);
  }

  if (Platform.isAndroid) {
    return 'http://10.0.2.2:8000/api/v1';
  }

  return 'http://192.168.0.108:8000/api/v1';
}

final appConfigProvider = Provider<AppConfig>((_) {
  return AppConfig(
    apiBaseUrl: _resolveApiBaseUrl(),
    connectTimeoutMs: 15000,
    receiveTimeoutMs: 25000,
    sendTimeoutMs: 15000,
  );
});
