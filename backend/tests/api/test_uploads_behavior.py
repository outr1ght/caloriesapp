from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.db.models.domain_enums import UploadStatus
from app.services.upload_service import UploadService


@pytest.mark.usefixtures("auth_overrides")
def test_upload_complete_negative_paths(client, monkeypatch):
    async def _init_upload(self, user_id, payload):
        _ = (self, user_id, payload)
        return {
            "upload_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "storage_key": "users/u/uploads/x.jpg",
            "upload_url": "https://example.com/upload",
            "upload_headers": {"Content-Type": "image/jpeg"},
            "expires_at": datetime.now(UTC).isoformat(),
        }

    async def _complete_not_found(self, user_id, upload_id):
        _ = (self, user_id, upload_id)
        raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.upload.not_found", status_code=404)

    monkeypatch.setattr(UploadService, "init_upload", _init_upload)
    monkeypatch.setattr(UploadService, "complete_upload", _complete_not_found)

    init_response = client.post(
        "/api/v1/uploads/init",
        json={
            "filename": "meal.jpg",
            "mime_type": "image/jpeg",
            "file_size": 1024,
            "sha256": "a" * 64,
        },
    )
    assert init_response.status_code == 200

    invalid_uuid = client.post("/api/v1/uploads/complete", json={"upload_id": "bad-id"})
    assert invalid_uuid.status_code == 422

    not_found = client.post("/api/v1/uploads/complete", json={"upload_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"})
    assert not_found.status_code == 404


@pytest.mark.usefixtures("auth_overrides")
def test_upload_complete_success(client, monkeypatch):
    async def _complete(self, user_id, upload_id):
        _ = (self, user_id, upload_id)
        return SimpleNamespace(
            id=upload_id,
            storage_key="users/u/uploads/x.jpg",
            status=UploadStatus.UPLOADED,
        )

    monkeypatch.setattr(UploadService, "complete_upload", _complete)
    response = client.post("/api/v1/uploads/complete", json={"upload_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"})
    assert response.status_code == 200
    assert response.json()["data"]["status"] == UploadStatus.UPLOADED.value
