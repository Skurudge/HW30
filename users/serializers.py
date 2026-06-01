from rest_framework import serializers
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Платежей."""
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор полного профиля для владельца (Задание 1)."""
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar", "payments")
        extra_kwargs = {
            "password": {"write_only": True}  # Пароль можно только передать при регистрации, но нельзя прочесть
        }


class UserPublicSerializer(serializers.ModelSerializer):
    """Сериализатор ограниченного профиля для чужих пользователей (Дополнительное задание)."""
    class Meta:
        model = User
        # Исключаем пароль, фамилию (в нашей модели её нет) и историю платежей
        fields = ("id", "email", "city", "avatar")
