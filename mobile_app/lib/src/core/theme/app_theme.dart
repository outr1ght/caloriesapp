import 'package:flutter/material.dart';

class AppTheme {
  static const _seed = Color(0xFF2F6B5F);

  static ThemeData get light => ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: _seed, brightness: Brightness.light),
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF7FAF8),
        cardTheme: const CardTheme(margin: EdgeInsets.zero),
      );

  static ThemeData get dark => ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: _seed, brightness: Brightness.dark),
        useMaterial3: true,
      );
}
