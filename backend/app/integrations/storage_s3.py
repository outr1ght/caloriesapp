from datetime import UTC, datetime, timedelta

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.common.exceptions import AppException, ErrorCode
from app.core.config import get_settings


class S3StorageService:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            region_name=settings.s3_region,
            aws_access_key_id=settings.s3_access_key_id,
            aws_secret_access_key=settings.s3_secret_access_key,
            use_ssl=settings.s3_use_ssl,
        )

    def create_presigned_upload(self, *, key: str, mime_type: str, expires_seconds: int = 900) -> dict:
        try:
            url = self.client.generate_presigned_url(
                ClientMethod="put_object",
                Params={"Bucket": self.settings.s3_bucket, "Key": key, "ContentType": mime_type},
                ExpiresIn=expires_seconds,
            )
        except (ClientError, BotoCoreError) as exc:
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc

        return {
            "upload_url": url,
            "upload_headers": {"Content-Type": mime_type},
            "expires_at": datetime.now(UTC) + timedelta(seconds=expires_seconds),
        }

    def object_exists(self, *, key: str) -> bool:
        try:
            self.client.head_object(Bucket=self.settings.s3_bucket, Key=key)
            return True
        except ClientError as exc:
            error_code = str(exc.response.get("Error", {}).get("Code", ""))
            if error_code in {"404", "NoSuchKey", "NotFound"}:
                return False
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc
        except BotoCoreError as exc:
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc
