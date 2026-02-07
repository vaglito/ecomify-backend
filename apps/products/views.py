from rest_framework import viewsets, pagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from .models import Product, Brand, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, SubCategorySerializer


# Define specific filters
class ProductFilter(filters.FilterSet):
    minPrice = filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = filters.CharFilter(field_name="category__slug")
    subcategory = filters.CharFilter(field_name="subcategory__slug")
    brand = filters.CharFilter(method="filter_by_multiple_brands")

    class Meta:
        model = Product
        fields = ["category", "subcategory", "brand", "minPrice", "maxPrice"]

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
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ["name", "description", "sku", "brand__name", "category__name", "subcategory__name"]
    ordering_fields = ["price", "created_at", "name", "statistics__visits"]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"  # For detail view to use /products/[slug]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Increment visits counter
        # Using get_or_create to ensure stats object exists
        from .models import ProductStatistics
        stats, _ = ProductStatistics.objects.get_or_create(product=instance)
        stats.visits += 1
        stats.save(update_fields=['visits', 'last_visit'])
        
        serializer = self.get_serializer(instance)
        from rest_framework.response import Response
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    pagination_class = None  # Disable pagination to get all categories


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all().order_by("name")
    serializer_class = SubCategorySerializer
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ["category__slug"] # Enable filtering subcategories by category


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    pagination_class = None  # Disable pagination to get all brands
