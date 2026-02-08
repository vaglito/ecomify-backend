from django.urls import path
from .views.jwt import EmailTokenObtainPairView
from .views.register import RegisterView
from .views.me import MeView
from .views.verification import VerifyEmailView
from .views.password_reset import PasswordResetRequestView, PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterView.as_view(), name="register_user"),
    path("verify-email/<str:uidb64>/<str:token>/", VerifyEmailView.as_view(), name="verify_email"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset-confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("me/", MeView.as_view(), name="me_view"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
