from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import AppException, ErrorCode
from app.core.upload_security import validate_upload
from app.db.models.meal import UploadedImage
from app.integrations.storage_s3 import S3StorageService
from app.schemas.uploads import UploadInitRequest


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

        if not self.storage.object_exists(key=entity.storage_key):
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.upload.object_not_found", status_code=409)

        metadata = entity.metadata_json or {}
        metadata["verified"] = True
        entity.metadata_json = metadata

        await self.session.commit()
        await self.session.refresh(entity)
        return entity
