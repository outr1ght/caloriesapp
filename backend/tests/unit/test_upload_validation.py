import pytest

from app.common.exceptions import AppException
from app.core.upload_security import validate_upload


def test_upload_validation_rejects_invalid_mime():
    with pytest.raises(AppException) as exc:
        validate_upload(filename="meal.jpg", mime_type="text/plain", file_size=128, sha256="a" * 64)
    assert exc.value.status_code == 422


def test_upload_validation_rejects_invalid_size():
    with pytest.raises(AppException) as exc:
        validate_upload(filename="meal.jpg", mime_type="image/jpeg", file_size=0, sha256="a" * 64)
    assert exc.value.status_code == 422
