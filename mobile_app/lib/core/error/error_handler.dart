import 'app_error.dart';

class ErrorHandler {
  const ErrorHandler();

  AppError map(Object error) {
    if (error is AppError) {
      return error;
    }

    return const AppError(message: 'unexpected_error');
  }
}
