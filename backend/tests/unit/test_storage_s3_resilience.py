from botocore.exceptions import ClientError

from app.integrations.storage_s3 import S3StorageService


def test_object_exists_not_found(monkeypatch):
    service = S3StorageService()

    def _head_object(Bucket, Key):
        _ = (Bucket, Key)
        raise ClientError({"Error": {"Code": "404"}}, "HeadObject")

    monkeypatch.setattr(service.client, "head_object", _head_object)
    assert service.object_exists(key="missing") is False
