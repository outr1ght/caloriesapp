from app.common.messages import MESSAGES
from app.db.models.enums import LanguageCode
from app.schemas.localization import SupportedLocaleDTO

class LocalizationService:
    SUPPORTED = [SupportedLocaleDTO(code=LanguageCode.EN, label="English"), SupportedLocaleDTO(code=LanguageCode.ES, label="Español"), SupportedLocaleDTO(code=LanguageCode.RU, label="Русский")]

    def get_supported_locales(self) -> list[SupportedLocaleDTO]:
        return self.SUPPORTED

    def resolve_messages(self, keys: list[str], locale: LanguageCode) -> dict[str, str]:
        _ = locale
        return {k: MESSAGES.get(k, k) for k in keys}
