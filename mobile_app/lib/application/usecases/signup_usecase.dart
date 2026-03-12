import '../../domain/entities/user_session.dart';
import '../../domain/repositories/auth_repository.dart';

class SignupUseCase {
  const SignupUseCase(this._repository);

  final AuthRepository _repository;

  Future<UserSession> call(String email, String password) {
    return _repository.signup(email, password);
  }
}
