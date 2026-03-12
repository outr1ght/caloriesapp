import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config/app_config.dart';
import '../error/app_error.dart';

final dioProvider = Provider<Dio>((ref) {
  final config = ref.read(appConfigProvider);

  final dio = Dio(
    BaseOptions(
      baseUrl: config.apiBaseUrl,
      connectTimeout: Duration(milliseconds: config.connectTimeoutMs),
      receiveTimeout: Duration(milliseconds: config.receiveTimeoutMs),
      sendTimeout: Duration(milliseconds: config.sendTimeoutMs),
      headers: const {'Content-Type': 'application/json'},
    ),
  );

  dio.interceptors.add(
    InterceptorsWrapper(
      onError: (error, handler) {
        final data = error.response?.data;
        String message = 'request_failed';
        String? code;

        if (data is Map<String, dynamic>) {
          final messageKey = data['message_key'];
          if (messageKey is String && messageKey.isNotEmpty) {
            message = messageKey;
          }

          final e = data['error'];
          if (e is Map<String, dynamic>) {
            final c = e['code'];
            if (c is String && c.isNotEmpty) {
              code = c;
            }
          }
        }

        handler.reject(
          DioException(
            requestOptions: error.requestOptions,
            response: error.response,
            type: error.type,
            error: AppError(message: message, code: code, statusCode: error.response?.statusCode),
          ),
        );
      },
    ),
  );

  return dio;
});
