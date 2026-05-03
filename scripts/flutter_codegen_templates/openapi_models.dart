// GENERATED CODE - DO NOT MODIFY BY HAND.
// Source: docs/openapi/openapi.json

class GeneratedApiEnvelope<T> {
  const GeneratedApiEnvelope({
    required this.ok,
    required this.messageKey,
    required this.data,
    required this.error,
    required this.meta,
  });

  final bool ok;
  final String messageKey;
  final T data;
  final Map<String, dynamic>? error;
  final Map<String, dynamic> meta;

  static GeneratedApiEnvelope<T> fromJson<T>(
    Map<String, dynamic> json,
    T Function(Object? raw) readData,
  ) {
    final meta = (json['meta'] as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
    final error = (json['error'] as Map?)?.cast<String, dynamic>();
    return GeneratedApiEnvelope<T>(
      ok: json['ok'] == true,
      messageKey: (json['message_key'] as String?) ?? '',
      data: readData(json['data']),
      error: error,
      meta: meta,
    );
  }
}

class GeneratedPaginationMeta {
  const GeneratedPaginationMeta({
    required this.page,
    required this.pageSize,
    required this.total,
    required this.totalPages,
  });

  final int page;
  final int pageSize;
  final int total;
  final int totalPages;

  factory GeneratedPaginationMeta.fromJson(Map<String, dynamic> json) {
    return GeneratedPaginationMeta(
      page: _readInt(json['page']),
      pageSize: _readInt(json['page_size']),
      total: _readInt(json['total']),
      totalPages: _readInt(json['total_pages']),
    );
  }
}

class GeneratedTokenPair {
  const GeneratedTokenPair({required this.accessToken, required this.refreshToken});

  final String accessToken;
  final String refreshToken;

  factory GeneratedTokenPair.fromJson(Map<String, dynamic> json) {
    return GeneratedTokenPair(
      accessToken: (json['access_token'] as String?) ?? '',
      refreshToken: (json['refresh_token'] as String?) ?? '',
    );
  }
}

class GeneratedAuthUser {
  const GeneratedAuthUser({required this.id, required this.email});

  final String id;
  final String email;

  factory GeneratedAuthUser.fromJson(Map<String, dynamic> json) {
    return GeneratedAuthUser(
      id: (json['id'] as String?) ?? '',
      email: (json['email'] as String?) ?? '',
    );
  }
}

class GeneratedAuthSession {
  const GeneratedAuthSession({required this.user, required this.tokens});

  final GeneratedAuthUser user;
  final GeneratedTokenPair tokens;

  factory GeneratedAuthSession.fromJson(Map<String, dynamic> json) {
    final user = (json['user'] as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
    final tokens = (json['tokens'] as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
    return GeneratedAuthSession(
      user: GeneratedAuthUser.fromJson(user),
      tokens: GeneratedTokenPair.fromJson(tokens),
    );
  }
}

class GeneratedMealNutritionSummary {
  const GeneratedMealNutritionSummary({
    required this.calories,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
  });

  final double calories;
  final double proteinG;
  final double carbsG;
  final double fatG;

  factory GeneratedMealNutritionSummary.fromJson(Map<String, dynamic> json) {
    return GeneratedMealNutritionSummary(
      calories: _readDouble(json['calories']),
      proteinG: _readDouble(json['protein_g']),
      carbsG: _readDouble(json['carbs_g']),
      fatG: _readDouble(json['fat_g']),
    );
  }
}

class GeneratedMealItem {
  const GeneratedMealItem({
    required this.id,
    required this.displayName,
    required this.quantity,
    required this.unit,
    required this.position,
    this.ingredientId,
    this.foodProductId,
  });

  final String id;
  final String? ingredientId;
  final String? foodProductId;
  final String displayName;
  final double quantity;
  final String unit;
  final int position;

  factory GeneratedMealItem.fromJson(Map<String, dynamic> json) {
    return GeneratedMealItem(
      id: (json['id'] as String?) ?? '',
      ingredientId: json['ingredient_id'] as String?,
      foodProductId: json['food_product_id'] as String?,
      displayName: (json['display_name'] as String?) ?? '',
      quantity: _readDouble(json['quantity']),
      unit: (json['unit'] as String?) ?? 'g',
      position: _readInt(json['position']),
    );
  }
}

class GeneratedMealImageReference {
  const GeneratedMealImageReference({
    required this.id,
    required this.storageKey,
    required this.mimeType,
    required this.fileSize,
    required this.status,
    required this.createdAt,
  });

  final String id;
  final String storageKey;
  final String mimeType;
  final int fileSize;
  final String status;
  final DateTime createdAt;

  factory GeneratedMealImageReference.fromJson(Map<String, dynamic> json) {
    return GeneratedMealImageReference(
      id: (json['id'] as String?) ?? '',
      storageKey: (json['storage_key'] as String?) ?? '',
      mimeType: (json['mime_type'] as String?) ?? '',
      fileSize: _readInt(json['file_size']),
      status: (json['status'] as String?) ?? '',
      createdAt: _readDateTime(json['created_at']),
    );
  }
}

class GeneratedMealRead {
  const GeneratedMealRead({
    required this.id,
    required this.userId,
    required this.title,
    required this.notes,
    required this.mealType,
    required this.source,
    required this.eatenAt,
    required this.analysisStatus,
    required this.nutritionSummary,
    required this.items,
    required this.images,
    required this.createdAt,
    required this.updatedAt,
  });

  final String id;
  final String userId;
  final String? title;
  final String? notes;
  final String mealType;
  final String source;
  final DateTime eatenAt;
  final String analysisStatus;
  final GeneratedMealNutritionSummary? nutritionSummary;
  final List<GeneratedMealItem> items;
  final List<GeneratedMealImageReference> images;
  final DateTime createdAt;
  final DateTime updatedAt;

  factory GeneratedMealRead.fromJson(Map<String, dynamic> json) {
    final nutrition = (json['nutrition_summary'] as Map?)?.cast<String, dynamic>();
    final items = (json['items'] as List?)?.whereType<Map>().map((x) => GeneratedMealItem.fromJson(x.cast<String, dynamic>())).toList() ?? const <GeneratedMealItem>[];
    final images = (json['images'] as List?)?.whereType<Map>().map((x) => GeneratedMealImageReference.fromJson(x.cast<String, dynamic>())).toList() ?? const <GeneratedMealImageReference>[];
    return GeneratedMealRead(
      id: (json['id'] as String?) ?? '',
      userId: (json['user_id'] as String?) ?? '',
      title: json['title'] as String?,
      notes: json['notes'] as String?,
      mealType: (json['meal_type'] as String?) ?? '',
      source: (json['source'] as String?) ?? '',
      eatenAt: _readDateTime(json['eaten_at']),
      analysisStatus: (json['analysis_status'] as String?) ?? '',
      nutritionSummary: nutrition == null ? null : GeneratedMealNutritionSummary.fromJson(nutrition),
      items: items,
      images: images,
      createdAt: _readDateTime(json['created_at']),
      updatedAt: _readDateTime(json['updated_at']),
    );
  }
}

class GeneratedMealListPage {
  const GeneratedMealListPage({required this.items, required this.meta});

  final List<GeneratedMealRead> items;
  final GeneratedPaginationMeta meta;

  factory GeneratedMealListPage.fromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List?)?.whereType<Map>().map((x) => GeneratedMealRead.fromJson(x.cast<String, dynamic>())).toList() ?? const <GeneratedMealRead>[];
    final meta = (json['meta'] as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
    return GeneratedMealListPage(items: items, meta: GeneratedPaginationMeta.fromJson(meta));
  }
}

class GeneratedLoginRequest {
  const GeneratedLoginRequest({required this.email, required this.password});

  final String email;
  final String password;

  Map<String, dynamic> toJson() => {'email': email, 'password': password};
}

class GeneratedRegisterRequest {
  const GeneratedRegisterRequest({required this.email, required this.password});

  final String email;
  final String password;

  Map<String, dynamic> toJson() => {'email': email, 'password': password};
}

class GeneratedLogoutRequest {
  const GeneratedLogoutRequest({required this.refreshToken});

  final String refreshToken;

  Map<String, dynamic> toJson() => {'refresh_token': refreshToken};
}

DateTime _readDateTime(Object? raw) {
  if (raw is String && raw.isNotEmpty) {
    return DateTime.tryParse(raw)?.toUtc() ?? DateTime.fromMillisecondsSinceEpoch(0, isUtc: true);
  }
  return DateTime.fromMillisecondsSinceEpoch(0, isUtc: true);
}

double _readDouble(Object? raw) {
  if (raw is num) return raw.toDouble();
  if (raw is String) return double.tryParse(raw) ?? 0;
  return 0;
}

int _readInt(Object? raw) {
  if (raw is int) return raw;
  if (raw is num) return raw.toInt();
  if (raw is String) return int.tryParse(raw) ?? 0;
  return 0;
}
