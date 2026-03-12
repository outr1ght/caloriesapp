import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/presentation/router/route_guard.dart';

RouteGuardState _state({
  String path = '/splash',
  bool authLoading = false,
  bool isAuthenticated = false,
  bool profileLoading = false,
  bool goalsLoading = false,
  bool isProfileComplete = false,
  bool hasGoal = false,
}) {
  return RouteGuardState(
    path: path,
    authLoading: authLoading,
    isAuthenticated: isAuthenticated,
    profileLoading: profileLoading,
    goalsLoading: goalsLoading,
    isProfileComplete: isProfileComplete,
    hasGoal: hasGoal,
  );
}

void main() {
  test('unauthenticated protected route redirects to login', () {
    final redirect = AppRouteGuard.redirect(_state(path: '/dashboard'));
    expect(redirect, '/login');
  });

  test('authenticated incomplete profile redirects to profile setup', () {
    final redirect = AppRouteGuard.redirect(
      _state(path: '/dashboard', isAuthenticated: true, isProfileComplete: false),
    );
    expect(redirect, '/profile-setup');
  });

  test('authenticated complete profile without goal redirects to goal setup', () {
    final redirect = AppRouteGuard.redirect(
      _state(path: '/dashboard', isAuthenticated: true, isProfileComplete: true, hasGoal: false),
    );
    expect(redirect, '/goal-setup');
  });

  test('authenticated completed user can access dashboard', () {
    final redirect = AppRouteGuard.redirect(
      _state(path: '/dashboard', isAuthenticated: true, isProfileComplete: true, hasGoal: true),
    );
    expect(redirect, isNull);
  });

  test('loading state routes to splash', () {
    final redirect = AppRouteGuard.redirect(
      _state(path: '/dashboard', authLoading: true),
    );
    expect(redirect, '/splash');
  });
}
