from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import settings
from app.core.deps import get_current_user_id
from app.schemas.meal import UploadImageResponse

router = APIRouter()


@router.post("/image", response_model=UploadImageResponse)
async def upload_image(file: UploadFile = File(...), user_id: str = Depends(get_current_user_id)) -> UploadImageResponse:
    allowed = set(x.strip() for x in settings.allowed_image_mime.split(","))
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported mime type")
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    return UploadImageResponse(image_id="img_demo", upload_url="s3://placeholder/img_demo")
