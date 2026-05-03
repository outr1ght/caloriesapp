from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PaginationMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)


def build_pagination_meta(page: int, page_size: int, total: int) -> PaginationMeta:
    total_pages = 0
    if total > 0:
        total_pages = (total + page_size - 1) // page_size
    return PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages)


def build_paginated_data(*, items: list[Any], page: int, page_size: int, total: int) -> dict[str, Any]:
    return {
        "items": items,
        "meta": build_pagination_meta(page=page, page_size=page_size, total=total).model_dump(),
    }
