from app.schemas.common import build_pagination_meta


def test_build_pagination_meta_with_items() -> None:
    meta = build_pagination_meta(page=2, page_size=20, total_items=95)
    assert meta.page == 2
    assert meta.total_pages == 5


def test_build_pagination_meta_empty() -> None:
    meta = build_pagination_meta(page=1, page_size=20, total_items=0)
    assert meta.total_pages == 0
