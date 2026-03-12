import '../../domain/entities/user_session.dart';
import '../../domain/repositories/auth_repository.dart';

class LoginUseCase {
  const LoginUseCase(this._repository);

  final AuthRepository _repository;

  Future<UserSession> call(String email, String password) {
    return _repository.login(email, password);
  }
}
