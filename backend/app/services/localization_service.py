from app.common.messages import resolve_message
from app.db.models.enums import LanguageCode
from app.schemas.localization import SupportedLocaleDTO


class LocalizationService:
    SUPPORTED = [
        SupportedLocaleDTO(code=LanguageCode.EN, label="English"),
        SupportedLocaleDTO(code=LanguageCode.ES, label="Espanol"),
        SupportedLocaleDTO(code=LanguageCode.DE, label="Deutsch"),
        SupportedLocaleDTO(code=LanguageCode.FR, label="Francais"),
        SupportedLocaleDTO(code=LanguageCode.RU, label="Russkii"),
    ]

    def get_supported_locales(self) -> list[SupportedLocaleDTO]:
        return self.SUPPORTED

    def resolve_messages(self, keys: list[str], locale: LanguageCode) -> dict[str, str]:
        return {key: resolve_message(key, locale) for key in keys}
