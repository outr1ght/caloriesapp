from app.db.models.enums import LanguageCode
from app.services.localization_service import LocalizationService


def test_language_code_enum_supports_mobile_locales() -> None:
    assert {LanguageCode.EN, LanguageCode.ES, LanguageCode.DE, LanguageCode.FR, LanguageCode.RU}


def test_localization_service_supports_mobile_locales() -> None:
    codes = {item.code for item in LocalizationService().get_supported_locales()}
    assert {LanguageCode.EN, LanguageCode.ES, LanguageCode.DE, LanguageCode.FR, LanguageCode.RU}.issubset(codes)
