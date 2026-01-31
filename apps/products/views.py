from rest_framework import viewsets, pagination
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from .models import Product, Brand, Category
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer


# Define specific filters
class ProductFilter(filters.FilterSet):
    minPrice = filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = filters.CharFilter(field_name="category__slug")
    brand = filters.CharFilter(method="filter_by_multiple_brands")

    class Meta:
        model = Product
        fields = ["category", "brand", "minPrice", "maxPrice"]

    # Allows filtering by multiple brands at once (?brand=ricoh,epson)
    def filter_by_multiple_brands(self, queryset, name, value):
        brands = value.split(",")
        return queryset.filter(brand__slug__in=brands)


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 12  # Matches frontend configuration
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = ProductFilter
    search_fields = ["name", "description", "sku", "brand__name", "category__name"]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"  # For detail view to use /products/[slug]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    pagination_class = None  # Disable pagination to get all categories


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    pagination_class = None  # Disable pagination to get all brands
