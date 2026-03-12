from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.models.nutrition import Barcode, FoodProduct, NutritionValue
from app.integrations.barcode_provider import BarcodeProvider, NullBarcodeProvider
from app.schemas.barcode import BarcodeLookupResponse

class BarcodeService:
    def __init__(self, session: AsyncSession, provider: BarcodeProvider | None = None) -> None:
        self.session = session
        self.provider = provider or NullBarcodeProvider()

    async def lookup(self, code: str) -> BarcodeLookupResponse:
        result = await self.session.execute(select(Barcode).where(Barcode.code == code).options(selectinload(Barcode.food_product).selectinload(FoodProduct.default_nutrition)))
        barcode = result.scalar_one_or_none()
        if barcode is not None:
            product = barcode.food_product
            return BarcodeLookupResponse(found=True, product={"product_id": product.id, "name": product.name, "brand": product.brand, "barcode": barcode.code})
        external = await self.provider.lookup(code)
        if external is None:
            return BarcodeLookupResponse(found=False, product=None)
        nv = NutritionValue(calories=Decimal(str(external["nutrition"]["calories"])), protein_g=Decimal(str(external["nutrition"]["protein_g"])), carbs_g=Decimal(str(external["nutrition"]["carbs_g"])), fat_g=Decimal(str(external["nutrition"]["fat_g"])), fiber_g=Decimal("0"), sugar_g=Decimal("0"), sodium_mg=Decimal("0"), source=external.get("source", "external"), confidence=Decimal("0.800"))
        self.session.add(nv)
        await self.session.flush()
        product = FoodProduct(name=external["name"], brand=external.get("brand"), source_name=external.get("source", "external"), source_product_id=str(external.get("product_id") or code), default_nutrition_value_id=nv.id)
        self.session.add(product)
        await self.session.flush()
        self.session.add(Barcode(code=code, food_product_id=product.id))
        await self.session.commit()
        return BarcodeLookupResponse(found=True, product={"product_id": product.id, "name": product.name, "brand": product.brand, "barcode": code})
