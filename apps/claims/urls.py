from rest_framework.routers import DefaultRouter
from .views import ClaimViewSet

router = DefaultRouter()
router.register(r'claims', ClaimViewSet, basename='claims')

urlpatterns = router.urls
