from django.urls import path
from .views.jwt import EmailTokenObtainPairView
from .views.register import RegisterView
from .views.me import MeView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterView.as_view(), name="register_user"),
    path("me/", MeView.as_view(), name="me_view"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
