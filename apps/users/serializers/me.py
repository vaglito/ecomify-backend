from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(read_only=True)
    is_staff_user = serializers.BooleanField(read_only=True)
    is_customer = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "is_active",
            "email",
            "first_name",
            "last_name",
            "is_admin",
            "is_staff_user",
            "is_customer",
            "created_at",
            "updated_at",
        ]
