from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт для редактирования профиля любого пользователя (Дополнительное задание)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    """
    Эндпоинт вывода списка платежей с фильтрацией и сортировкой (Задание 4).
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Подключаем бэкенды фильтрации и сортировки DRF
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Настраиваем поля для точной фильтрации согласно ТЗ
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')

    # Настраиваем сортировку по дате оплаты (позволяет передавать ?ordering=payment_date или ?ordering=-payment_date)
    ordering_fields = ('payment_date',)
