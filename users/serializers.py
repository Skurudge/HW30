from rest_framework import serializers
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Платежей с финтех-полями Stripe (Задание 2)."""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор полного профиля для владельца."""
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar", "payments")
        extra_kwargs = {"password": {"write_only": True}}


class UserPublicSerializer(serializers.ModelSerializer):
    """Сериализатор ограниченного профиля для чужих пользователей."""
    class Meta:
        model = User
        fields = ("id", "email", "city", "avatar")
