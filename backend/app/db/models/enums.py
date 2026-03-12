from enum import StrEnum


class LocaleCode(StrEnum):
    EN = "en"
    ES = "es"
    DE = "de"
    FR = "fr"
    RU = "ru"


class UnitSystem(StrEnum):
    METRIC = "metric"
    IMPERIAL = "imperial"


class BiologicalSex(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ActivityLevel(StrEnum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class MealType(StrEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class AuthProvider(StrEnum):
    PASSWORD = "password"
    GOOGLE = "google"
    APPLE = "apple"


class RecommendationType(StrEnum):
    LOW_PROTEIN = "low_protein"
    HIGH_CALORIES = "high_calories"
    UNBALANCED_MACROS = "unbalanced_macros"
    UNDER_EATING = "under_eating"
    OVER_EATING = "over_eating"
