from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )

        if not user:
            # Check if user exists but is inactive
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                check_user = User.objects.get(email=email)
                if not check_user.is_active:
                    raise AuthenticationFailed("user_inactive")
            except User.DoesNotExist:
                pass
            
            raise AuthenticationFailed("invalid_credentials")

        data = super().validate(attrs)

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
            "is_customer": user.is_customer,
            "is_staff_user": user.is_staff_user,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        return data
