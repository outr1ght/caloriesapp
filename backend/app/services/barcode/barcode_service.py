from app.schemas.features import BarcodeScanResponse


class BarcodeService:
    def scan(self, code: str) -> BarcodeScanResponse:
        if code == "737628064502":
            return BarcodeScanResponse(
                found=True,
                product_name="Organic Peanut Butter",
                brand="Sample Foods",
                nutrition_per_100g={"calories": 588, "protein_g": 25, "fat_g": 50, "carbs_g": 20},
            )
        return BarcodeScanResponse(found=False)


barcode_service = BarcodeService()
