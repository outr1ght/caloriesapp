import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

final localeProvider = StateNotifierProvider<LocaleNotifier, Locale?>((_) => LocaleNotifier());

class LocaleNotifier extends StateNotifier<Locale?> {
  LocaleNotifier() : super(null) {
    _restore();
  }

  static const _key = 'locale_code_v1';

  Future<void> _restore() async {
    final prefs = await SharedPreferences.getInstance();
    final code = prefs.getString(_key);
    if (code == null || code.isEmpty) return;
    state = Locale(code);
  }

  Future<void> setLocale(String? code) async {
    final prefs = await SharedPreferences.getInstance();
    if (code == null || code.isEmpty) {
      state = null;
      await prefs.remove(_key);
      return;
    }

    state = Locale(code);
    await prefs.setString(_key, code);
  }
}
