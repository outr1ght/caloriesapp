from fastapi import APIRouter

router = APIRouter()


@router.get("/supported-languages")
def supported_languages() -> dict[str, list[str]]:
    return {"languages": ["en", "es", "de", "fr", "ru"]}
