class BarcodeProductEntity {
  const BarcodeProductEntity({
    required this.productId,
    required this.name,
    required this.brand,
    required this.barcode,
  });

  final String productId;
  final String name;
  final String brand;
  final String barcode;
}

class BarcodeLookupEntity {
  const BarcodeLookupEntity({required this.found, this.product});

  final bool found;
  final BarcodeProductEntity? product;
}
