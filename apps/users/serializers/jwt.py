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
            raise AuthenticationFailed("invalid credentials")

        data = super().validate(attrs)

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_customer": user.is_customer,
            "is_staff_user": user.is_staff_user,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        return data
