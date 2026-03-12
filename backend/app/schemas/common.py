from pydantic import BaseModel, Field


class PaginationMeta(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


def build_pagination_meta(page: int, page_size: int, total_items: int) -> PaginationMeta:
    total_pages = 0
    if total_items > 0:
        total_pages = (total_items + page_size - 1) // page_size
    return PaginationMeta(page=page, page_size=page_size, total_items=total_items, total_pages=total_pages)
