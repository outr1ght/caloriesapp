from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class AuthProvider(StrEnum):
    LOCAL = "local"
    GOOGLE = "google"
    APPLE = "apple"


class LanguageCode(StrEnum):
    EN = "en"
    ES = "es"
    RU = "ru"
