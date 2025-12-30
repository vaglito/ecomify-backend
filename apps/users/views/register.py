from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from ..serializers.register import RegisterSerializer

User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
