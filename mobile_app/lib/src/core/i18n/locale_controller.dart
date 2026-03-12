import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

final localeControllerProvider = StateNotifierProvider<LocaleController, Locale?>((ref) {
  return LocaleController();
});

class LocaleController extends StateNotifier<Locale?> {
  LocaleController() : super(null) {
    _restore();
  }

  static const _localeKey = 'app_locale_code';

  Future<void> _restore() async {
    final prefs = await SharedPreferences.getInstance();
    final code = prefs.getString(_localeKey);
    if (code != null && code.isNotEmpty) {
      state = Locale(code);
    }
  }

  Future<void> setLocale(String? code) async {
    final prefs = await SharedPreferences.getInstance();

    if (code == null || code.isEmpty) {
      state = null;
      await prefs.remove(_localeKey);
      return;
    }

    state = Locale(code);
    await prefs.setString(_localeKey, code);
  }
}
