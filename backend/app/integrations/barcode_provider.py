from typing import Protocol


class BarcodeProductResult(dict):
    pass


class BarcodeProvider(Protocol):
    async def lookup(self, barcode: str) -> BarcodeProductResult | None:
        ...


class NullBarcodeProvider:
    async def lookup(self, barcode: str) -> BarcodeProductResult | None:
        return None
