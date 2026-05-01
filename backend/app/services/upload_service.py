from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.core.logging import get_logger
from app.core.upload_security import validate_upload
from app.db.models.meal import UploadedImage
from app.integrations.storage_s3 import S3StorageService
from app.schemas.uploads import UploadInitRequest

logger = get_logger(__name__)


class UploadService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.storage = S3StorageService()

    async def init_upload(self, user_id: str, payload: UploadInitRequest) -> dict:
        validate_upload(
            filename=payload.filename,
            mime_type=payload.mime_type,
            file_size=payload.file_size,
            sha256=payload.sha256,
        )

        upload_id = str(uuid4())
        ext = payload.filename.split(".")[-1].lower()
        storage_key = f"users/{user_id}/uploads/{upload_id}.{ext}"

        image = UploadedImage(
            id=upload_id,
            user_id=user_id,
            meal_id=payload.meal_id,
            storage_key=storage_key,
            mime_type=payload.mime_type.lower(),
            file_size=payload.file_size,
            sha256=payload.sha256.lower(),
        )
        self.session.add(image)
        await self.session.commit()

        presigned = self.storage.create_presigned_upload(key=storage_key, mime_type=payload.mime_type.lower())
        return {
            "upload_id": upload_id,
            "storage_key": storage_key,
            "upload_url": presigned["upload_url"],
            "upload_headers": presigned["upload_headers"],
            "expires_at": presigned["expires_at"],
        }

    async def complete_upload(self, user_id: str, upload_id: str) -> UploadedImage:
        entity = await self.session.get(UploadedImage, upload_id)
        if entity is None or entity.user_id != user_id or entity.deleted_at is not None:
            raise AppException(code=ErrorCode.NOT_FOUND, message_key="errors.upload.not_found", status_code=404)

        try:
            metadata = self.storage.get_object_metadata(key=entity.storage_key)
            if metadata is None:
                logger.warning(
                    "uploaded object missing during completion",
                    extra={"event": {"event_name": "upload_object_missing", "upload_id": entity.id, "storage_key": entity.storage_key}},
                )
                raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.upload.object_not_found", status_code=409)

            actual_size = metadata.get("size")
            if actual_size is not None and int(actual_size) != entity.file_size:
                cleanup_deleted = self.storage.delete_object(key=entity.storage_key)
                logger.warning(
                    "uploaded object size mismatch",
                    extra={
                        "event": {
                            "event_name": "upload_size_mismatch",
                            "upload_id": entity.id,
                            "storage_key": entity.storage_key,
                            "expected_size": entity.file_size,
                            "actual_size": int(actual_size),
                            "cleanup_attempted": True,
                            "cleanup_deleted": cleanup_deleted,
                        }
                    },
                )
                raise AppException(code=ErrorCode.CONFLICT, message_key="errors.upload.invalid_file_size", status_code=409)

            actual_sha256 = self.storage.compute_object_sha256(key=entity.storage_key)
            if actual_sha256 is None:
                logger.warning(
                    "uploaded object missing during checksum verification",
                    extra={"event": {"event_name": "upload_object_missing", "upload_id": entity.id, "storage_key": entity.storage_key}},
                )
                raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.upload.object_not_found", status_code=409)

            if actual_sha256.lower() != entity.sha256.lower():
                cleanup_deleted = self.storage.delete_object(key=entity.storage_key)
                logger.warning(
                    "uploaded object checksum mismatch",
                    extra={
                        "event": {
                            "event_name": "upload_checksum_mismatch",
                            "upload_id": entity.id,
                            "storage_key": entity.storage_key,
                            "cleanup_attempted": True,
                            "cleanup_deleted": cleanup_deleted,
                        }
                    },
                )
                raise AppException(code=ErrorCode.CONFLICT, message_key="errors.upload.invalid_checksum", status_code=409)

            metadata_json = entity.metadata_json or {}
            metadata_json["verified"] = True
            entity.metadata_json = metadata_json

            await self.session.commit()
            await self.session.refresh(entity)
            return entity
        except AppException as exc:
            log_method = logger.error if exc.status_code >= 500 else logger.warning
            log_method(
                "upload completion failed",
                exc_info=exc if exc.status_code >= 500 else None,
                extra={
                    "event": {
                        "event_name": "upload_completion_failed",
                        "upload_id": entity.id,
                        "storage_key": entity.storage_key,
                        "status_code": exc.status_code,
                        "message_key": exc.message_key,
                    }
                },
            )
            raise
