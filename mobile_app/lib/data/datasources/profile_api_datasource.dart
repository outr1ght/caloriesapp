import 'package:shared_preferences/shared_preferences.dart';

import '../../core/network/api_client.dart';

class ProfileApiDatasource {
  ProfileApiDatasource(this._client);

  final ApiClient _client;
  static const _activityKey = 'profile_activity_level_v1';

  Future<Map<String, dynamic>> getMe() async {
    final response = await _client.get<Map<String, dynamic>>('/me');
    return response.data ?? <String, dynamic>{};
  }

  Future<Map<String, dynamic>> listWeights() async {
    final response = await _client.get<Map<String, dynamic>>('/weights', queryParameters: {'page': 1, 'page_size': 1});
    return response.data ?? <String, dynamic>{};
  }

  Future<void> updateProfile({
    required String firstName,
    required String lastName,
    required int age,
    required String gender,
    required double heightCm,
  }) async {
    final birthYear = DateTime.now().year - age;
    await _client.patch<Map<String, dynamic>>(
      '/me/profile',
      data: {
        'first_name': firstName,
        'last_name': lastName,
        'birth_year': birthYear,
        'gender': gender,
        'height_cm': heightCm,
      },
    );
  }

  Future<void> createWeight(double value) async {
    await _client.post<Map<String, dynamic>>(
      '/weights',
      data: {
        'logged_at': DateTime.now().toUtc().toIso8601String(),
        'weight_kg': value,
      },
    );
  }

  Future<void> saveActivityLevel(String activityLevel) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_activityKey, activityLevel);
  }

  Future<String> getActivityLevel() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_activityKey) ?? 'moderate';
  }
}
