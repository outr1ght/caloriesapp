import '../domain/auth_repository.dart';
import '../domain/auth_session.dart';

class LoginUseCase {
  const LoginUseCase(this._repo);

  final AuthRepository _repo;

  Future<AuthSession> call(String email, String password) => _repo.login(email, password);
}
