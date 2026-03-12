import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../config/app_config.dart';
import '../storage/session_storage.dart';
import 'api_client.dart';
import 'api_error.dart';

final secureStorageProvider = Provider<FlutterSecureStorage>((_) => const FlutterSecureStorage());

final sessionStorageProvider = Provider<SessionStorage>((ref) {
  return SessionStorage(ref.read(secureStorageProvider));
});

final dioProvider = Provider<Dio>((ref) {
  final config = ref.read(appConfigProvider);

  final dio = Dio(
    BaseOptions(
      baseUrl: config.apiBaseUrl,
      connectTimeout: Duration(milliseconds: config.connectTimeoutMs),
      receiveTimeout: Duration(milliseconds: config.receiveTimeoutMs),
      sendTimeout: Duration(milliseconds: config.sendTimeoutMs),
      headers: {'Content-Type': 'application/json'},
    ),
  );

  dio.interceptors.add(
    InterceptorsWrapper(
      onError: (error, handler) {
        final response = error.response;
        String message = 'Request failed';
        String? code;

        final data = response?.data;
        if (data is Map<String, dynamic>) {
          final messageKey = data['message_key'];
          if (messageKey is String && messageKey.isNotEmpty) {
            message = messageKey;
          }

          final errorData = data['error'];
          if (errorData is Map<String, dynamic>) {
            final c = errorData['code'];
            if (c is String && c.isNotEmpty) code = c;
          }
        }

        handler.reject(
          DioException(
            requestOptions: error.requestOptions,
            response: response,
            type: error.type,
            error: ApiError(
              message: message,
              statusCode: response?.statusCode,
              code: code,
            ),
          ),
        );
      },
    ),
  );

  return dio;
});

final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient(ref.read(dioProvider), ref.read(sessionStorageProvider));
});
