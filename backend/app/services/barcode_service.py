from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.nutrition import Barcode, FoodProduct, NutritionValue
from app.integrations.barcode_provider import BarcodeProvider, NullBarcodeProvider
from app.schemas.barcode import BarcodeLookupResponse


class _ExternalNutrition(BaseModel):
    model_config = ConfigDict(extra="ignore")
    calories: Decimal = Field(ge=0)
    protein_g: Decimal = Field(ge=0)
    carbs_g: Decimal = Field(ge=0)
    fat_g: Decimal = Field(ge=0)


class _ExternalBarcodePayload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = Field(min_length=1, max_length=255)
    brand: str | None = Field(default=None, max_length=255)
    source: str = Field(default="external", min_length=1, max_length=64)
    product_id: str | None = Field(default=None, max_length=128)
    nutrition: _ExternalNutrition


class BarcodeService:
    def __init__(self, session: AsyncSession, provider: BarcodeProvider | None = None) -> None:
        self.session = session
        self.provider = provider or NullBarcodeProvider()

    async def lookup(self, code: str) -> BarcodeLookupResponse:
        result = await self.session.execute(
            select(Barcode)
            .where(Barcode.code == code)
            .options(selectinload(Barcode.food_product).selectinload(FoodProduct.default_nutrition))
        )
        barcode = result.scalar_one_or_none()
        if barcode is not None:
            product = barcode.food_product
            return BarcodeLookupResponse(
                found=True,
                product={
                    "product_id": product.id,
                    "name": product.name,
                    "brand": product.brand,
                    "barcode": barcode.code,
                },
            )

        try:
            external_raw = await self.provider.lookup(code)
        except Exception:
            return BarcodeLookupResponse(found=False, product=None)

        if external_raw is None:
            return BarcodeLookupResponse(found=False, product=None)

        try:
            external = _ExternalBarcodePayload.model_validate(dict(external_raw))
        except (ValidationError, TypeError, ValueError):
            return BarcodeLookupResponse(found=False, product=None)

        nv = NutritionValue(
            calories=external.nutrition.calories,
            protein_g=external.nutrition.protein_g,
            carbs_g=external.nutrition.carbs_g,
            fat_g=external.nutrition.fat_g,
            fiber_g=Decimal("0"),
            sugar_g=Decimal("0"),
            sodium_mg=Decimal("0"),
            source=external.source,
            confidence=Decimal("0.800"),
        )
        self.session.add(nv)
        await self.session.flush()

        product = FoodProduct(
            name=external.name,
            brand=external.brand,
            source_name=external.source,
            source_product_id=external.product_id or code,
            default_nutrition_value_id=nv.id,
        )
        self.session.add(product)
        await self.session.flush()

        self.session.add(Barcode(code=code, food_product_id=product.id))
        await self.session.commit()

        return BarcodeLookupResponse(
            found=True,
            product={
                "product_id": product.id,
                "name": product.name,
                "brand": product.brand,
                "barcode": code,
            },
        )
