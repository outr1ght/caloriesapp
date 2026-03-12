import 'package:dio/dio.dart';

import '../../domain/entities/user_session.dart';
import '../storage/token_storage.dart';

class ApiClient {
  ApiClient(this._dio, this._tokenStorage);

  final Dio _dio;
  final TokenStorage _tokenStorage;

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

  Future<void> applySession(UserSession? session) async {
    if (session == null) {
      _dio.options.headers.remove('Authorization');
      await _tokenStorage.clear();
      return;
    }

    _dio.options.headers['Authorization'] = 'Bearer ${session.accessToken}';
    await _tokenStorage.save(session);
  }
}
