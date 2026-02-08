from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from apps.core.utils.emails import send_html_email

User = get_user_model()

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "El email es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Link to frontend
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

            # Send email
            context = {
                "user": user,
                "reset_url": reset_url,
            }
            send_html_email(
                subject="Recuperación de Contraseña - Ecomify",
                template_name="emails/password_reset.html",
                context=context,
                to_email=user.email,
            )
        except User.DoesNotExist:
            # For security, don't reveal if user exists or not
            pass
            
        return Response(
            {"message": "Si el correo existe en nuestra base de datos, recibirás un enlace para restablecer tu contraseña."},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get("password")
        if not password:
            return Response({"error": "La nueva contraseña es requerida."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message": "Contraseña restablecida exitosamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "El enlace es inválido o ha expirado."}, status=status.HTTP_400_BAD_REQUEST)
