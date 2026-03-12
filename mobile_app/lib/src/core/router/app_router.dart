import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/application/auth_controller.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/barcode/presentation/barcode_screen.dart';
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/diary/presentation/food_diary_screen.dart';
import '../../features/goals/presentation/calorie_goal_setup_screen.dart';
import '../../features/meals/presentation/analysis_screen.dart';
import '../../features/meals/presentation/capture_screen.dart';
import '../../features/onboarding/presentation/onboarding_screen.dart';
import '../../features/profile_setup/presentation/profile_setup_screen.dart';
import '../../features/recommendations/presentation/recommendations_screen.dart';
import '../../features/reports/presentation/reports_screen.dart';
import '../../features/settings/presentation/settings_screen.dart';
import '../../features/splash/presentation/splash_screen.dart';

final appRouterProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authControllerProvider);

  const publicRoutes = <String>{'/', '/login', '/splash'};

  return GoRouter(
    initialLocation: '/splash',
    redirect: (context, state) {
      final location = state.matchedLocation;
      final isLoading = authState.isLoading;
      final isAuthenticated = authState.valueOrNull != null;
      final isPublic = publicRoutes.contains(location);

      if (isLoading) {
        return location == '/splash' ? null : '/splash';
      }

      if (!isAuthenticated) {
        if (!isPublic) return '/login';
        if (location == '/splash') return '/';
        return null;
      }

      if (location == '/login' || location == '/' || location == '/splash') {
        return '/dashboard';
      }

      return null;
    },
    routes: [
      GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
      GoRoute(path: '/', builder: (_, __) => const OnboardingScreen()),
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/profile-setup', builder: (_, __) => const ProfileSetupScreen()),
      GoRoute(path: '/goal-setup', builder: (_, __) => const CalorieGoalSetupScreen()),
      GoRoute(path: '/dashboard', builder: (_, __) => const DashboardScreen()),
      GoRoute(path: '/capture', builder: (_, __) => const CaptureScreen()),
      GoRoute(path: '/analysis', builder: (_, __) => const AnalysisScreen()),
      GoRoute(path: '/diary', builder: (_, __) => const FoodDiaryScreen()),
      GoRoute(path: '/reports', builder: (_, __) => const ReportsScreen()),
      GoRoute(path: '/recommendations', builder: (_, __) => const RecommendationsScreen()),
      GoRoute(path: '/barcode', builder: (_, __) => const BarcodeScreen()),
      GoRoute(path: '/settings', builder: (_, __) => const SettingsScreen()),
    ],
  );
});
