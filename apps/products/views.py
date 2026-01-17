from rest_framework import viewsets, pagination
from django_filters import rest_framework as filters
from .models import Producto, Marca, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer, MarcaSerializer


# Definimos los filtros específicos
class ProductoFilter(filters.FilterSet):
    minPrice = filters.NumberFilter(field_name="precio", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="precio", lookup_expr="lte")
    categoria = filters.CharFilter(field_name="categoria__slug")
    marca = filters.CharFilter(method="filter_by_multiple_marcas")

    class Meta:
        model = Producto
        fields = ["categoria", "marca", "minPrice", "maxPrice"]

    # Permite filtrar por varias marcas a la vez (?marca=ricoh,epson)
    def filter_by_multiple_marcas(self, queryset, name, value):
        marcas = value.split(",")
        return queryset.filter(marca__slug__in=marcas)


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 12  # Coincide con lo que pusimos en el frontend
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all().order_by("-fecha_creacion")
    serializer_class = ProductoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductoFilter
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"  # Para que el detalle use /products/[slug]


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all().order_by("nombre")
    serializer_class = CategoriaSerializer
    pagination_class = None  # Desactivamos paginación para obtener todas


class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.all().order_by("nombre")
    serializer_class = MarcaSerializer
    pagination_class = None  # Desactivamos paginación para obtener toda
