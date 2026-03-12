class RouteGuardState {
  const RouteGuardState({
    required this.path,
    required this.authLoading,
    required this.isAuthenticated,
    required this.profileLoading,
    required this.goalsLoading,
    required this.isProfileComplete,
    required this.hasGoal,
  });

  final String path;
  final bool authLoading;
  final bool isAuthenticated;
  final bool profileLoading;
  final bool goalsLoading;
  final bool isProfileComplete;
  final bool hasGoal;
}

class AppRouteGuard {
  static const publicRoutes = {'/splash', '/onboarding', '/login', '/signup'};

  static String? redirect(RouteGuardState s) {
    final isPublic = publicRoutes.contains(s.path);

    if (s.authLoading) {
      return s.path == '/splash' ? null : '/splash';
    }

    if (!s.isAuthenticated) {
      if (!isPublic) return '/login';
      if (s.path == '/splash') return '/onboarding';
      return null;
    }

    if (s.path == '/login' || s.path == '/signup' || s.path == '/onboarding') {
      return '/dashboard';
    }

    if (s.profileLoading || s.goalsLoading) {
      return s.path == '/splash' ? null : '/splash';
    }

    if (!s.isProfileComplete) {
      return s.path == '/profile-setup' ? null : '/profile-setup';
    }

    if (!s.hasGoal) {
      return s.path == '/goal-setup' ? null : '/goal-setup';
    }

    if (s.path == '/profile-setup' || s.path == '/goal-setup' || s.path == '/splash') {
      return '/dashboard';
    }

    return null;
  }
}
