import hashlib
from datetime import UTC, datetime, timedelta

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.common.exceptions import AppException, ErrorCode
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


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
            logger.error(
                "storage operation failed",
                exc_info=exc,
                extra={"event": {"event_name": "upload_storage_error", "operation": "create_presigned_upload", "storage_key": key}},
            )
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
            logger.error(
                "storage operation failed",
                exc_info=exc,
                extra={"event": {"event_name": "upload_storage_error", "operation": "head_object", "storage_key": key, "error_code": error_code}},
            )
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc
        except BotoCoreError as exc:
            logger.error(
                "storage operation failed",
                exc_info=exc,
                extra={"event": {"event_name": "upload_storage_error", "operation": "head_object", "storage_key": key}},
            )
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc

    def get_object_metadata(self, *, key: str) -> dict | None:
        try:
            response = self.client.head_object(Bucket=self.settings.s3_bucket, Key=key)
            return {
                "size": int(response.get("ContentLength", 0)),
                "content_type": response.get("ContentType"),
            }
        except ClientError as exc:
            error_code = str(exc.response.get("Error", {}).get("Code", ""))
            if error_code in {"404", "NoSuchKey", "NotFound"}:
                return None
            logger.error(
                "storage operation failed",
                exc_info=exc,
                extra={"event": {"event_name": "upload_storage_error", "operation": "head_object", "storage_key": key, "error_code": error_code}},
            )
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc
        except BotoCoreError as exc:
            logger.error(
                "storage operation failed",
                exc_info=exc,
                extra={"event": {"event_name": "upload_storage_error", "operation": "head_object", "storage_key": key}},
            )
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc

    def compute_object_sha256(self, *, key: str, chunk_size: int = 1024 * 1024) -> str | None:
        body = None
        try:
            response = self.client.get_object(Bucket=self.settings.s3_bucket, Key=key)
            body = response["Body"]
            hasher = hashlib.sha256()
            while chunk := body.read(chunk_size):
                hasher.update(chunk)
            return hasher.hexdigest()
        except ClientError as exc:
            error_code = str(exc.response.get("Error", {}).get("Code", ""))
            if error_code in {"404", "NoSuchKey", "NotFound"}:
                return None
            logger.error(
                "storage operation failed",
                exc_info=exc,
                extra={"event": {"event_name": "upload_storage_error", "operation": "get_object", "storage_key": key, "error_code": error_code}},
            )
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc
        except BotoCoreError as exc:
            logger.error(
                "storage operation failed",
                exc_info=exc,
                extra={"event": {"event_name": "upload_storage_error", "operation": "get_object", "storage_key": key}},
            )
            raise AppException(
                code=ErrorCode.INTERNAL_ERROR,
                message_key="errors.upload.storage_unavailable",
                status_code=503,
            ) from exc
        finally:
            if body is not None:
                body.close()

    def delete_object(self, *, key: str) -> bool:
        try:
            self.client.delete_object(Bucket=self.settings.s3_bucket, Key=key)
            return True
        except (ClientError, BotoCoreError) as exc:
            logger.error(
                "storage operation failed",
                exc_info=exc,
                extra={"event": {"event_name": "upload_storage_error", "operation": "delete_object", "storage_key": key}},
            )
            return False
