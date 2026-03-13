import 'package:dio/dio.dart';

import '../../domain/entities/user_session.dart';
import '../storage/token_storage.dart';

class ApiClient {
  ApiClient(this._dio, this._tokenStorage);

  final Dio _dio;
  final TokenStorage _tokenStorage;

  Future<Response<T>> get<T>(String path, {Map<String, dynamic>? queryParameters}) {
    return _requestWithRefresh<T>(() => _dio.get<T>(path, queryParameters: queryParameters), path: path);
  }

  Future<Response<T>> post<T>(String path, {Object? data}) {
    return _requestWithRefresh<T>(() => _dio.post<T>(path, data: data), path: path);
  }

  Future<Response<T>> patch<T>(String path, {Object? data}) {
    return _requestWithRefresh<T>(() => _dio.patch<T>(path, data: data), path: path);
  }

  Future<Response<T>> delete<T>(String path) {
    return _requestWithRefresh<T>(() => _dio.delete<T>(path), path: path);
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

  Future<Response<T>> _requestWithRefresh<T>(Future<Response<T>> Function() request, {required String path}) async {
    try {
      return await request();
    } on DioException catch (error) {
      final status = error.response?.statusCode;
      final isAuthEndpoint = path.startsWith('/auth/');
      if (status != 401 || isAuthEndpoint) rethrow;

      final refreshed = await _refreshSession();
      if (!refreshed) rethrow;
      return request();
    }
  }

  Future<bool> _refreshSession() async {
    final current = await _tokenStorage.read();
    if (current == null || current.refreshToken.isEmpty) {
      await applySession(null);
      return false;
    }

    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/auth/refresh',
        data: {'refresh_token': current.refreshToken},
      );

      final root = response.data ?? <String, dynamic>{};
      final data = (root['data'] as Map<String, dynamic>?) ?? root;

      final accessToken = (data['access_token'] as String?) ?? '';
      final refreshToken = (data['refresh_token'] as String?) ?? '';
      if (accessToken.isEmpty || refreshToken.isEmpty) {
        await applySession(null);
        return false;
      }

      await applySession(UserSession(accessToken: accessToken, refreshToken: refreshToken));
      return true;
    } catch (_) {
      await applySession(null);
      return false;
    }
  }
}
