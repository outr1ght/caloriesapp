class RecommendationEntity {
  const RecommendationEntity({
    required this.id,
    required this.title,
    required this.status,
    required this.type,
  });

  final String id;
  final String title;
  final String status;
  final String type;
}
