from django.urls import path
from users.apps import UsersConfig
from users.views import UserUpdateAPIView, PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    # Обновление профиля пользователя (Дополнительное задание)
    path("profile/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_profile_update"),

    # Список платежей с фильтрацией и сортировкой (Задание 4)
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
]
