import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../application/providers/auth_provider.dart';
import '../../application/providers/goals_provider.dart';
import '../../application/providers/profile_provider.dart';
import '../features/auth/login_screen.dart';
import '../features/auth/signup_screen.dart';
import '../features/auth/splash_screen.dart';
import '../features/barcode_scan/barcode_scan_screen.dart';
import '../features/dashboard/dashboard_screen.dart';
import '../features/food_diary/food_diary_screen.dart';
import '../features/food_diary/meal_detail_screen.dart';
import '../features/goals/goal_setup_screen.dart';
import '../features/meal_analysis/meal_analysis_screen.dart';
import '../features/meal_capture/camera_capture_screen.dart';
import '../features/meal_capture/meal_capture_screen.dart';
import '../features/meal_capture/photo_preview_screen.dart';
import '../features/meal_planner/meal_planner_screen.dart';
import '../features/onboarding/onboarding_screen.dart';
import '../features/profile/profile_setup_screen.dart';
import '../features/recommendations/recommendations_screen.dart';
import '../features/reports/reports_screen.dart';
import '../features/settings/settings_screen.dart';
import '../features/weight_tracking/weight_tracking_screen.dart';

final goRouterProvider = Provider<GoRouter>((ref) {
  final auth = ref.watch(authStateProvider);
  final isAuthenticated = auth.valueOrNull != null;
  final profile = isAuthenticated ? ref.watch(profileProvider) : const AsyncData(null);
  final goals = isAuthenticated ? ref.watch(goalsProvider) : const AsyncData(null);

  return GoRouter(
    initialLocation: '/splash',
    redirect: (context, state) {
      final path = state.matchedLocation;
      const publicRoutes = {'/splash', '/onboarding', '/login', '/signup'};
      final isPublic = publicRoutes.contains(path);

      if (auth.isLoading) {
        return path == '/splash' ? null : '/splash';
      }

      if (!isAuthenticated) {
        if (!isPublic) return '/login';
        if (path == '/splash') return '/onboarding';
        return null;
      }

      if (path == '/login' || path == '/signup' || path == '/onboarding') {
        return '/dashboard';
      }

      if (profile.isLoading || goals.isLoading) {
        return path == '/splash' ? null : '/splash';
      }

      final isProfileComplete = profile.valueOrNull != null;
      if (!isProfileComplete && path != '/profile-setup') {
        return '/profile-setup';
      }

      if (isProfileComplete) {
        final hasGoal = goals.valueOrNull != null;
        if (!hasGoal && path != '/goal-setup') {
          return '/goal-setup';
        }
      }

      if ((path == '/profile-setup' && isProfileComplete) || (path == '/goal-setup' && goals.valueOrNull != null)) {
        return '/dashboard';
      }

      if (path == '/splash') return '/dashboard';
      return null;
    },
    routes: [
      GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
      GoRoute(path: '/onboarding', builder: (_, __) => const OnboardingScreen()),
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/signup', builder: (_, __) => const SignupScreen()),
      GoRoute(path: '/profile-setup', builder: (_, __) => const ProfileSetupScreen()),
      GoRoute(path: '/goal-setup', builder: (_, __) => const GoalSetupScreen()),
      GoRoute(path: '/dashboard', builder: (_, __) => const DashboardScreen()),
      GoRoute(path: '/meal-capture', builder: (_, __) => const MealCaptureScreen()),
      GoRoute(path: '/meal-capture/camera', builder: (_, __) => const CameraCaptureScreen()),
      GoRoute(
        path: '/meal-capture/preview',
        builder: (_, state) {
          final imagePath = state.extra;
          if (imagePath is! String) return const MealCaptureScreen();
          return PhotoPreviewScreen(path: imagePath);
        },
      ),
      GoRoute(
        path: '/meal-analysis',
        builder: (_, state) {
          final imageId = state.extra is String ? state.extra as String : null;
          return MealAnalysisScreen(uploadedImageId: imageId);
        },
      ),
      GoRoute(path: '/food-diary', builder: (_, __) => const FoodDiaryScreen()),
      GoRoute(path: '/food-diary/meal/:id', builder: (_, s) => MealDetailScreen(mealId: s.pathParameters['id']!)),
      GoRoute(path: '/reports', builder: (_, __) => const ReportsScreen()),
      GoRoute(path: '/recommendations', builder: (_, __) => const RecommendationsScreen()),
      GoRoute(path: '/meal-planner', builder: (_, __) => const MealPlannerScreen()),
      GoRoute(path: '/barcode-scan', builder: (_, __) => const BarcodeScanScreen()),
      GoRoute(path: '/weight-tracking', builder: (_, __) => const WeightTrackingScreen()),
      GoRoute(path: '/settings', builder: (_, __) => const SettingsScreen()),
    ],
  );
});
