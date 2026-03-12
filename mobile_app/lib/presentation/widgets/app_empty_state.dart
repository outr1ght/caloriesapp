import 'package:flutter/material.dart';

class AppEmptyState extends StatelessWidget {
  const AppEmptyState({super.key, required this.message});

  final String message;

  @override
  Widget build(BuildContext context) => Center(child: Text(message));
}
