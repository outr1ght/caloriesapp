import 'package:dio/dio.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

import '../network/api_error.dart';

class ErrorHandler {
  const ErrorHandler();

  String toMessage(Object error, AppLocalizations l10n) {
    if (error is DioException && error.error is ApiError) {
      final apiError = error.error as ApiError;
      if (apiError.code == 'AUTH_UNAUTHORIZED' || apiError.code == 'AUTH_INVALID_TOKEN') {
        return l10n.loginFailedMessage;
      }
      return l10n.unexpectedErrorMessage;
    }

    if (error is ApiError) {
      if (error.code == 'AUTH_UNAUTHORIZED' || error.code == 'AUTH_INVALID_TOKEN') {
        return l10n.loginFailedMessage;
      }
    }

    return l10n.unexpectedErrorMessage;
  }
}
