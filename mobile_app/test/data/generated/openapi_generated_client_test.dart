import 'package:flutter_test/flutter_test.dart';

import 'package:calories_mobile/data/api/generated/generated.dart';

import '../../helpers/test_helpers.dart';

void main() {
  test('generated auth api parses login envelope', () async {
    final apiClient = DummyApiClient();
    apiClient.postResponses['/auth/login'] = {
      'ok': true,
      'message_key': 'messages.common.success',
      'data': {
        'user': {'id': 'u1', 'email': 'u@example.com'},
        'tokens': {'access_token': 'a1', 'refresh_token': 'r1'},
      },
      'error': null,
      'meta': {},
    };

    final api = GeneratedAuthApi(apiClient);
    final session = await api.login(const GeneratedLoginRequest(email: 'u@example.com', password: 'secret'));

    expect(session.user.id, 'u1');
    expect(session.tokens.accessToken, 'a1');
    expect(session.tokens.refreshToken, 'r1');
  });

  test('generated meals api parses pagination and meal dto', () async {
    final apiClient = DummyApiClient();
    apiClient.getResponses['/meals'] = {
      'ok': true,
      'message_key': 'messages.common.success',
      'data': {
        'items': [
          {
            'id': 'm1',
            'user_id': 'u1',
            'title': 'Chicken bowl',
            'notes': null,
            'meal_type': 'lunch',
            'source': 'manual',
            'eaten_at': '2026-05-02T12:34:56Z',
            'analysis_status': 'ready',
            'nutrition_summary': {
              'calories': '600',
              'protein_g': '40',
              'carbs_g': '50',
              'fat_g': '20'
            },
            'items': [],
            'images': [],
            'created_at': '2026-05-02T12:34:56Z',
            'updated_at': '2026-05-02T12:34:56Z'
          }
        ],
        'meta': {'page': 1, 'page_size': 20, 'total': 1, 'total_pages': 1}
      },
      'error': null,
      'meta': {},
    };

    final api = GeneratedMealsApi(apiClient);
    final page = await api.listMeals();

    expect(page.meta.total, 1);
    expect(page.items.single.mealType, 'lunch');
    expect(page.items.single.nutritionSummary?.calories, 600);
    expect(page.items.single.eatenAt.toUtc().toIso8601String(), '2026-05-02T12:34:56.000Z');
  });
}
