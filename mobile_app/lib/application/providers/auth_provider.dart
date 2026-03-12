import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/auth_repository_impl.dart';
import '../../domain/entities/user_session.dart';
import '../usecases/login_usecase.dart';
import '../usecases/logout_usecase.dart';
import '../usecases/signup_usecase.dart';

final authStateProvider = AsyncNotifierProvider<AuthController, UserSession?>(AuthController.new);

class AuthController extends AsyncNotifier<UserSession?> {
  @override
  Future<UserSession?> build() async {
    return ref.read(authRepositoryProvider).restoreSession();
  }

  Future<void> login(String email, String password) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = LoginUseCase(ref.read(authRepositoryProvider));
      return usecase(email, password);
    });
  }

  Future<void> signup(String email, String password) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final usecase = SignupUseCase(ref.read(authRepositoryProvider));
      return usecase(email, password);
    });
  }

  Future<void> logout() async {
    final usecase = LogoutUseCase(ref.read(authRepositoryProvider));
    await usecase();
    state = const AsyncData(null);
  }
}
