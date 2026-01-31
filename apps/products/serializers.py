from rest_framework import serializers
from .models import Product, Category, Brand, ProductImage, Specification


# 1. Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


# 2. Brand Serializer
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug"]


# 3. Product Image Gallery Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "order"]


# 4. Technical Specifications Serializer (Key-Value)
class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ["id", "content", "order"]


# 5. Main Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    # Nested relationships (read from related models)
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)

    # Read-only fields to show names instead of IDs
    category_name = serializers.ReadOnlyField(source="category.name")
    brand_name = serializers.ReadOnlyField(source="brand.name")

    # Dynamic calculation of discount percentage for the frontend
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "original_price",
            "discount_percentage",
            "sku",
            "stock",
            "is_new",
            "on_sale",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "images",
            "specifications",
            "created_at",
        ]

    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            discount = ((obj.original_price - obj.price) / obj.original_price) * 100
            return round(discount)
        return 0
