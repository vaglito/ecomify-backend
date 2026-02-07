from rest_framework import serializers
from .models import Product, Category, SubCategory, Brand, ProductImage, Specification


# 1. SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name", "slug", "category"]


# 2. Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    # Nested subcategories
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "subcategories"]


# 3. Brand Serializer
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "image"]


# 4. Product Image Gallery Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "order"]


# 5. Technical Specifications Serializer (Key-Value)
class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ["id", "content", "order"]


# 6. Main Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    # Nested relationships (read from related models)
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    # Read-only fields to show names instead of IDs
    category_name = serializers.ReadOnlyField(source="category.name")
    subcategory_name = serializers.ReadOnlyField(source="subcategory.name", allow_null=True)
    brand_name = serializers.ReadOnlyField(source="brand.name")

    # Dynamic calculation of discount percentage for the frontend
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "image",
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
            "subcategory",
            "subcategory_name",
            "brand",
            "brand_name",
            "images",
            "specifications",
            "meta_title",
            "meta_keywords",
            "created_at",
            "views_count",
            "sales_count",
        ]

    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            discount = ((obj.original_price - obj.price) / obj.original_price) * 100
            return round(discount)
        return 0

    # Fields to expose flattening statistics
    def get_views_count(self, obj):
        if hasattr(obj, "statistics"):
            return obj.statistics.visits
        return 0

    def get_sales_count(self, obj):
        if hasattr(obj, "statistics"):
            return obj.statistics.sales
        return 0

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url
        return None

    views_count = serializers.SerializerMethodField()
    sales_count = serializers.SerializerMethodField()
