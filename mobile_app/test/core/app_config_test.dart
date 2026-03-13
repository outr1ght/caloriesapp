import 'package:calories_mobile/core/config/app_config.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('default API base url contains /api/v1', () {
    final container = ProviderContainer();
    addTearDown(container.dispose);

    final config = container.read(appConfigProvider);
    expect(config.apiBaseUrl, contains('/api/v1'));
  });
}
