from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializers import UserSerializer, UserPublicSerializer, PaymentSerializer
from users.permissions import IsOwner


class UserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт открытой регистрации новых пользователей (Урок 31)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        email = serializer.validated_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError({"email": "Пользователь с таким email уже зарегистрирован."})
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Эндпоинт для просмотра и изменения профиля пользователя (Урок 31)."""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            profile_pk = self.kwargs.get("pk")
            if str(self.request.user.pk) == str(profile_pk):
                return UserSerializer
        return UserPublicSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Эндпоинт вывода списка платежей с фильтрацией и сортировкой (Урок 30.2)."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)
