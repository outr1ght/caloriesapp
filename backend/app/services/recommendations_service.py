from uuid import uuid4

from app.schemas.features import RecommendationResponse


class RecommendationService:
    def latest(self, locale: str) -> RecommendationResponse:
        text = {
            "en": "You are low on protein this week. Add one high-protein snack daily.",
            "es": "Esta semana te falta proteina. Agrega un snack alto en proteina al dia.",
            "de": "Diese Woche ist Ihr Eiweiss niedrig. Fugen Sie taglich einen proteinreichen Snack hinzu.",
            "fr": "Votre apport en proteines est faible cette semaine. Ajoutez une collation proteinee par jour.",
            "ru": "На этой неделе мало белка. Добавьте один белковый перекус в день.",
        }.get(locale, "Keep balanced meals and hydration.")
        return RecommendationResponse(id=str(uuid4()), locale=locale, summary=text)


recommendation_service = RecommendationService()
