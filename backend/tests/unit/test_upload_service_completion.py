from types import SimpleNamespace

import pytest

from app.common.exceptions import AppException, ErrorCode
from app.services.upload_service import UploadService


class FakeSession:
    def __init__(self, entity):
        self.entity = entity
        self.commits = 0
        self.refreshed = []

    async def get(self, model, upload_id):
        _ = (model, upload_id)
        return self.entity

    def add(self, entity):
        _ = entity

    async def commit(self):
        self.commits += 1

    async def refresh(self, entity):
        self.refreshed.append(entity)


class FakeStorage:
    def __init__(self, *, metadata=None, checksum=None, metadata_error=None, checksum_error=None, delete_result=True):
        self.metadata = metadata
        self.checksum = checksum
        self.metadata_error = metadata_error
        self.checksum_error = checksum_error
        self.delete_result = delete_result
        self.deleted_keys = []

    def get_object_metadata(self, *, key: str):
        _ = key
        if self.metadata_error is not None:
            raise self.metadata_error
        return self.metadata

    def compute_object_sha256(self, *, key: str):
        _ = key
        if self.checksum_error is not None:
            raise self.checksum_error
        return self.checksum

    def delete_object(self, *, key: str) -> bool:
        self.deleted_keys.append(key)
        return self.delete_result


def make_entity():
    return SimpleNamespace(
        id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        user_id="11111111-1111-1111-1111-111111111111",
        deleted_at=None,
        storage_key="users/u/uploads/x.jpg",
        file_size=4,
        sha256="3a6eb0790f39ac87c94f3856b2dd2c5d110e6811602261a9a923d3bb23adc8b7",
        metadata_json={},
    )


@pytest.mark.asyncio
async def test_complete_upload_missing_object(monkeypatch):
    entity = make_entity()
    session = FakeSession(entity)
    storage = FakeStorage(metadata=None)
    monkeypatch.setattr("app.services.upload_service.S3StorageService", lambda: storage)

    with pytest.raises(AppException) as exc:
        await UploadService(session).complete_upload(entity.user_id, entity.id)

    assert exc.value.status_code == 409
    assert exc.value.message_key == "errors.upload.object_not_found"
    assert storage.deleted_keys == []
    assert session.commits == 0


@pytest.mark.asyncio
async def test_complete_upload_size_mismatch_triggers_cleanup(monkeypatch):
    entity = make_entity()
    session = FakeSession(entity)
    storage = FakeStorage(metadata={"size": 9, "content_type": "image/jpeg"})
    monkeypatch.setattr("app.services.upload_service.S3StorageService", lambda: storage)

    with pytest.raises(AppException) as exc:
        await UploadService(session).complete_upload(entity.user_id, entity.id)

    assert exc.value.code == ErrorCode.CONFLICT
    assert exc.value.status_code == 409
    assert exc.value.message_key == "errors.upload.invalid_file_size"
    assert storage.deleted_keys == [entity.storage_key]
    assert session.commits == 0


@pytest.mark.asyncio
async def test_complete_upload_checksum_mismatch_triggers_cleanup(monkeypatch):
    entity = make_entity()
    session = FakeSession(entity)
    storage = FakeStorage(metadata={"size": entity.file_size, "content_type": "image/jpeg"}, checksum="b" * 64)
    monkeypatch.setattr("app.services.upload_service.S3StorageService", lambda: storage)

    with pytest.raises(AppException) as exc:
        await UploadService(session).complete_upload(entity.user_id, entity.id)

    assert exc.value.code == ErrorCode.CONFLICT
    assert exc.value.status_code == 409
    assert exc.value.message_key == "errors.upload.invalid_checksum"
    assert storage.deleted_keys == [entity.storage_key]
    assert session.commits == 0


@pytest.mark.asyncio
async def test_complete_upload_storage_failure_passthrough(monkeypatch):
    entity = make_entity()
    session = FakeSession(entity)
    storage_error = AppException(code=ErrorCode.INTERNAL_ERROR, message_key="errors.upload.storage_unavailable", status_code=503)
    storage = FakeStorage(metadata_error=storage_error)
    monkeypatch.setattr("app.services.upload_service.S3StorageService", lambda: storage)

    with pytest.raises(AppException) as exc:
        await UploadService(session).complete_upload(entity.user_id, entity.id)

    assert exc.value.status_code == 503
    assert exc.value.message_key == "errors.upload.storage_unavailable"
    assert storage.deleted_keys == []
    assert session.commits == 0


@pytest.mark.asyncio
async def test_complete_upload_success_marks_entity_verified(monkeypatch):
    entity = make_entity()
    session = FakeSession(entity)
    storage = FakeStorage(metadata={"size": entity.file_size, "content_type": "image/jpeg"}, checksum=entity.sha256)
    monkeypatch.setattr("app.services.upload_service.S3StorageService", lambda: storage)

    result = await UploadService(session).complete_upload(entity.user_id, entity.id)

    assert result is entity
    assert entity.metadata_json["verified"] is True
    assert storage.deleted_keys == []
    assert session.commits == 1
    assert session.refreshed == [entity]
