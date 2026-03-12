import '../entities/user_session.dart';

abstract class AuthRepository {
  Future<UserSession> login(String email, String password);
  Future<UserSession> signup(String email, String password);
  Future<UserSession?> restoreSession();
  Future<void> logout();
}
