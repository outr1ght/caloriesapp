from enum import StrEnum


class MealType(StrEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    OTHER = "other"


class MealSource(StrEnum):
    MANUAL = "manual"
    BARCODE = "barcode"
    IMAGE_ANALYSIS = "image_analysis"
    IMPORTED = "imported"


class AnalysisStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class RecommendationType(StrEnum):
    MEAL_ADJUSTMENT = "meal_adjustment"
    DAILY_SUMMARY = "daily_summary"
    GOAL_ALIGNMENT = "goal_alignment"
    HYDRATION = "hydration"


class RecommendationStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    DISMISSED = "dismissed"
    APPLIED = "applied"


class GoalStrategy(StrEnum):
    MAINTAIN = "maintain"
    LOSE = "lose"
    GAIN = "gain"


class ActivityLevel(StrEnum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class UploadStatus(StrEnum):
    UPLOADED = "uploaded"
    SCANNED = "scanned"
    REJECTED = "rejected"


class MealPlanStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class UnitSystem(StrEnum):
    METRIC = "metric"
    IMPERIAL = "imperial"


class AuditAction(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
