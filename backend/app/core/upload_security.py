import re

from app.common.exceptions import AppException, ErrorCode
from app.core.config import get_settings

_SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")
_FILENAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,255}$")


def validate_upload(*, filename: str, mime_type: str, file_size: int, sha256: str) -> None:
    settings = get_settings()
    if not _FILENAME_RE.match(filename):
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.upload.invalid_filename", status_code=422)
    if mime_type.lower() not in {m.lower() for m in settings.allowed_upload_mime}:
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.upload.invalid_mime_type", status_code=422)
    if file_size <= 0 or file_size > settings.max_upload_bytes:
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.upload.invalid_file_size", status_code=422)
    if not _SHA256_RE.match(sha256):
        raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.upload.invalid_checksum", status_code=422)
