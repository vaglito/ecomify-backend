from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SiteSetting
from .serializers import SiteSettingSerializer

class SiteSettingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        setting = SiteSetting.load()
        serializer = SiteSettingSerializer(setting)
        return Response(serializer.data)
