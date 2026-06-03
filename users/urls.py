from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserProfileAPIView,
    PaymentListAPIView
)

app_name = UsersConfig.name

urlpatterns = [
    # Аутентификация JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Пользователи
    path("register/", UserCreateAPIView.as_view(), name="user_register"),
    path("profile/<int:pk>/", UserProfileAPIView.as_view(), name="user_profile_detail"),

    # Платежи
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
]
