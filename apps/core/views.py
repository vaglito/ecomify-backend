from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SiteSetting, Banner
from .serializers import SiteSettingSerializer, BannerSerializer
from rest_framework import viewsets

class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer

class SiteSettingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        setting = SiteSetting.load()
        serializer = SiteSettingSerializer(setting)
        return Response(serializer.data)
