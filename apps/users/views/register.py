from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from ..serializers.register import RegisterSerializer
from apps.core.utils.emails import send_html_email

User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False  # Deactivate until verified
        user.save()

        # Generate verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Link to frontend (which will then call our backend verification endpoint)
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

        # Send email
        context = {
            "user": user,
            "verification_url": verification_url,
        }
        send_html_email(
            subject="Verifica tu cuenta en Ecomify",
            template_name="emails/verification.html",
            context=context,
            to_email=user.email,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {
                "message": "Usuario registrado exitosamente. Por favor, revisa tu correo para activar tu cuenta."
            },
            status=status.HTTP_201_CREATED,
        )
