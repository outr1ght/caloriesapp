from datetime import UTC, datetime, timedelta

import boto3

from app.core.config import get_settings


class S3StorageService:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.client = boto3.client("s3", endpoint_url=settings.s3_endpoint_url, region_name=settings.s3_region, aws_access_key_id=settings.s3_access_key_id, aws_secret_access_key=settings.s3_secret_access_key, use_ssl=settings.s3_use_ssl)

    def create_presigned_upload(self, *, key: str, mime_type: str, expires_seconds: int = 900) -> dict:
        url = self.client.generate_presigned_url(ClientMethod="put_object", Params={"Bucket": self.settings.s3_bucket, "Key": key, "ContentType": mime_type}, ExpiresIn=expires_seconds)
        return {"upload_url": url, "upload_headers": {"Content-Type": mime_type}, "expires_at": datetime.now(UTC) + timedelta(seconds=expires_seconds)}
