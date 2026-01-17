from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, MarcaViewSet, CategoriaViewSet

router = DefaultRouter()
router.register(r"productos", ProductoViewSet)
router.register(r"categorias", CategoriaViewSet)
router.register(r"marcas", MarcaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
