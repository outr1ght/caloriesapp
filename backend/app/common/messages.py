from app.db.models.enums import LanguageCode

MESSAGES: dict[str, dict[str, str]] = {
    "messages.common.success": {
        "en": "Success",
        "es": "Exito",
        "de": "Erfolg",
        "fr": "Succes",
        "ru": "Uspeshno",
    },
    "messages.health.ok": {
        "en": "Service is healthy",
        "es": "Servicio saludable",
        "de": "Dienst ist gesund",
        "fr": "Service operationnel",
        "ru": "Servis rabotaet",
    },
    "errors.common.internal": {
        "en": "Internal server error",
        "es": "Error interno del servidor",
        "de": "Interner Serverfehler",
        "fr": "Erreur interne du serveur",
        "ru": "Vnutrennyaya oshibka servera",
    },
    "errors.common.rate_limited": {
        "en": "Too many requests",
        "es": "Demasiadas solicitudes",
        "de": "Zu viele Anfragen",
        "fr": "Trop de requetes",
        "ru": "Slishkom mnogo zaprosov",
    },
    "errors.validation.invalid_request": {
        "en": "Request validation failed",
        "es": "Validacion de solicitud fallida",
        "de": "Validierung fehlgeschlagen",
        "fr": "Validation de la requete echouee",
        "ru": "Oshibka validatsii zaprosa",
    },
    "errors.validation.invalid_uuid": {
        "en": "Invalid identifier format",
        "es": "Formato de identificador invalido",
        "de": "Ungueltiges ID-Format",
        "fr": "Format d'identifiant invalide",
        "ru": "Nekorrektnyi format identifikatora",
    },
    "errors.auth.missing_credentials": {
        "en": "Authentication credentials are required",
        "es": "Se requieren credenciales de autenticacion",
        "de": "Authentifizierungsdaten sind erforderlich",
        "fr": "Identifiants d'authentification requis",
        "ru": "Trebuetsya autentifikatsiya",
    },
    "errors.auth.invalid_token": {
        "en": "Invalid token",
        "es": "Token invalido",
        "de": "Ungueltiges Token",
        "fr": "Jeton invalide",
        "ru": "Nekorrektny token",
    },
    "errors.auth.invalid_token_type": {
        "en": "Invalid token type",
        "es": "Tipo de token invalido",
        "de": "Ungueltiger Tokentyp",
        "fr": "Type de jeton invalide",
        "ru": "Neverny tip tokena",
    },
    "errors.auth.user_not_found": {
        "en": "Authenticated user not found",
        "es": "Usuario autenticado no encontrado",
        "de": "Authentifizierter Benutzer nicht gefunden",
        "fr": "Utilisateur authentifie introuvable",
        "ru": "Polzovatel ne naiden",
    },
    "errors.auth.refresh_revoked": {
        "en": "Refresh token has been revoked",
        "es": "El token de actualizacion fue revocado",
        "de": "Refresh-Token wurde widerrufen",
        "fr": "Le jeton de rafraichissement a ete revoque",
        "ru": "Refresh token otozvan",
    },
    "errors.auth.session_store_unavailable": {
        "en": "Session store is temporarily unavailable",
        "es": "El almacenamiento de sesiones no esta disponible",
        "de": "Session-Speicher ist voruebergehend nicht verfuegbar",
        "fr": "Le stockage de session est temporairement indisponible",
        "ru": "Khranilishche sessii vremenno nedostupno",
    },
    "errors.upload.object_not_found": {
        "en": "Uploaded object not found in storage",
        "es": "No se encontro el objeto cargado en almacenamiento",
        "de": "Hochgeladenes Objekt nicht im Speicher gefunden",
        "fr": "Objet televerse introuvable dans le stockage",
        "ru": "Zagruzhennyi obekt ne naiden v khranilishche",
    },
    "errors.upload.storage_unavailable": {
        "en": "File storage is temporarily unavailable",
        "es": "El almacenamiento de archivos no esta disponible",
        "de": "Dateispeicher ist voruebergehend nicht verfuegbar",
        "fr": "Le stockage de fichiers est temporairement indisponible",
        "ru": "Khranilishche failov vremenno nedostupno",
    },
    "errors.reports.invalid_date_range": {
        "en": "Invalid report date range",
        "es": "Rango de fechas del informe invalido",
        "de": "Ungueltiger Berichtszeitraum",
        "fr": "Plage de dates du rapport invalide",
        "ru": "Nekorrektnyi diapazon dat dlya otcheta",
    },
    "errors.reports.range_too_large": {
        "en": "Report date range is too large",
        "es": "El rango de fechas del informe es demasiado grande",
        "de": "Berichtszeitraum ist zu gross",
        "fr": "La plage de dates du rapport est trop grande",
        "ru": "Slishkom bolshoi diapazon dat dlya otcheta",
    },
}


def resolve_message(message_key: str, locale: LanguageCode) -> str:
    bucket = MESSAGES.get(message_key)
    if not bucket:
        return message_key
    return bucket.get(locale.value) or bucket.get(LanguageCode.EN.value) or message_key
