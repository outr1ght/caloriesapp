import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../application/providers/auth_provider.dart';
import '../../widgets/app_button.dart';
import '../../widgets/app_text_field.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final authState = ref.watch(authStateProvider);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.loginTitle)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          AppTextField(controller: _emailController, label: l10n.emailLabel),
          const SizedBox(height: 12),
          AppTextField(controller: _passwordController, label: l10n.passwordLabel, obscureText: true),
          const SizedBox(height: 16),
          AppButton(
            label: l10n.loginAction,
            onPressed: authState.isLoading
                ? null
                : () async {
                    await ref.read(authStateProvider.notifier).login(
                          _emailController.text.trim(),
                          _passwordController.text,
                        );
                    if (mounted && ref.read(authStateProvider).valueOrNull != null) {
                      context.go('/dashboard');
                    }
                  },
          ),
          TextButton(
            onPressed: () => context.go('/signup'),
            child: Text(l10n.createAccountAction),
          ),
        ],
      ),
    );
  }
}
