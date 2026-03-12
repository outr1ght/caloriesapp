import '../../domain/entities/recommendation_entity.dart';

class RecommendationModel {
  const RecommendationModel({
    required this.id,
    required this.title,
    required this.status,
    required this.type,
  });

  final String id;
  final String title;
  final String status;
  final String type;

  factory RecommendationModel.fromJson(Map<String, dynamic> json) {
    return RecommendationModel(
      id: (json['id'] as String?) ?? '',
      title: (json['title'] as String?) ?? '',
      status: (json['status'] as String?) ?? 'pending',
      type: (json['type'] as String?) ?? 'daily_summary',
    );
  }

  RecommendationEntity toEntity() {
    return RecommendationEntity(id: id, title: title, status: status, type: type);
  }
}
