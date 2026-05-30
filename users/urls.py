from django.urls import path
from users.apps import UsersConfig
from users.views import UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    # Эндпоинт редактирования профиля (Дополнительное задание)
    path("profile/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_profile_update"),
]
