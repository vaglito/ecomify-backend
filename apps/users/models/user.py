from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.users.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.groups.filter(name="admin").exists()

    @property
    def is_staff_user(self):
        return self.groups.filter(name="staff").exists()

    @property
    def is_customer(self):
        return self.groups.filter(name="customer").exists()
