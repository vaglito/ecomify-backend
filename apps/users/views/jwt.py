from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers.jwt import EmailTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
