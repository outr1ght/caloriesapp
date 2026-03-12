import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../storage/session_storage.dart';
import '../../features/auth/domain/auth_session.dart';

final apiBaseUrlProvider = Provider<String>((_) => 'http://localhost:8000/api/v1');

class ApiClient {
  ApiClient(this._dio, this._sessionStorage);

  final Dio _dio;
  final SessionStorage _sessionStorage;

  Future<Response<T>> get<T>(String path, {Map<String, dynamic>? queryParameters}) {
    return _dio.get<T>(path, queryParameters: queryParameters);
  }

  Future<Response<T>> post<T>(String path, {Object? data}) {
    return _dio.post<T>(path, data: data);
  }

  Future<Response<T>> patch<T>(String path, {Object? data}) {
    return _dio.patch<T>(path, data: data);
  }

  Future<Response<T>> delete<T>(String path) {
    return _dio.delete<T>(path);
  }

  Future<void> setSession(AuthSession? session) async {
    if (session == null) {
      _dio.options.headers.remove('Authorization');
      await _sessionStorage.clear();
      return;
    }

    _dio.options.headers['Authorization'] = 'Bearer ${session.accessToken}';
    await _sessionStorage.save(session);
  }
}
