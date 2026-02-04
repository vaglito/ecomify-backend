from django.urls import path
from .views import SiteSettingView, BannerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banner')

urlpatterns = [
    path('settings/', SiteSettingView.as_view(), name='site-settings'),
] + router.urls
