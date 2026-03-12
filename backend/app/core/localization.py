from fastapi import Header

LOCALES = {"en", "es", "de", "fr", "ru"}

MESSAGES = {
    "en": {"auth.invalid": "Invalid credentials", "nutrition.approximate": "Nutrition values are approximate."},
    "es": {"auth.invalid": "Credenciales invalidas", "nutrition.approximate": "Los valores nutricionales son aproximados."},
    "de": {"auth.invalid": "Ungultige Anmeldedaten", "nutrition.approximate": "Nahrwerte sind ungefahr."},
    "fr": {"auth.invalid": "Identifiants invalides", "nutrition.approximate": "Les valeurs nutritionnelles sont approximatives."},
    "ru": {"auth.invalid": "Неверные учетные данные", "nutrition.approximate": "Значения пищевой ценности приблизительны."},
}


def resolve_locale(accept_language: str | None) -> str:
    if not accept_language:
        return "en"
    first = accept_language.split(",")[0].split("-")[0].strip().lower()
    return first if first in LOCALES else "en"


def t(key: str, locale: str) -> str:
    return MESSAGES.get(locale, MESSAGES["en"]).get(key, key)


def locale_from_header(accept_language: str | None = Header(default=None)) -> str:
    return resolve_locale(accept_language)
