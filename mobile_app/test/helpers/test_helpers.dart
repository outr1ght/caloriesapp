import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'package:calories_mobile/core/network/api_client.dart';
import 'package:calories_mobile/core/storage/token_storage.dart';
import 'package:calories_mobile/domain/entities/user_session.dart';

class InMemoryTokenStorage extends TokenStorage {
  InMemoryTokenStorage() : super(const FlutterSecureStorage());

  UserSession? _session;

  @override
  Future<void> save(UserSession session) async {
    _session = session;
  }

  @override
  Future<UserSession?> read() async => _session;

  @override
  Future<void> clear() async {
    _session = null;
  }
}

class DummyApiClient extends ApiClient {
  DummyApiClient() : super(Dio(), InMemoryTokenStorage());

  final Map<String, dynamic> getResponses = {};
  final Map<String, dynamic> postResponses = {};
  final Map<String, dynamic> patchResponses = {};
  final Map<String, dynamic> deleteResponses = {};

  @override
  Future<Response<T>> get<T>(String path, {Map<String, dynamic>? queryParameters}) async {
    return Response<T>(
      requestOptions: RequestOptions(path: path),
      data: getResponses[path] as T?,
    );
  }

  @override
  Future<Response<T>> post<T>(String path, {Object? data}) async {
    return Response<T>(
      requestOptions: RequestOptions(path: path),
      data: postResponses[path] as T?,
    );
  }

  @override
  Future<Response<T>> patch<T>(String path, {Object? data}) async {
    return Response<T>(
      requestOptions: RequestOptions(path: path),
      data: patchResponses[path] as T?,
    );
  }

  @override
  Future<Response<T>> delete<T>(String path) async {
    return Response<T>(
      requestOptions: RequestOptions(path: path),
      data: deleteResponses[path] as T?,
    );
  }

  @override
  Future<void> applySession(UserSession? session) async {}
}
