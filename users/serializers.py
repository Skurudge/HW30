from rest_framework import serializers
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Платежей (Задание 4)."""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор профиля с вложенной историей платежей (Дополнительное задание)."""

    # Подтягиваем список всех платежей этого пользователя
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "payments")
