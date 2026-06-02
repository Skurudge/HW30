from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view  # Импорт документирования (Задание 1)

from users.models import User, Payment
from users.serializers import UserSerializer, UserPublicSerializer, PaymentSerializer
from users.permissions import IsOwner
from materials.services import StripeService  # Подключаем финтех-слой (Задание 2)


class UserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт открытой регистрации новых пользователей."""
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
    """Эндпоинт для просмотра и изменения профиля пользователя."""
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
    """Эндпоинт вывода списка платежей с фильтрацией и сортировкой."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)


@extend_schema_view(
    post=extend_schema(
        summary="Инициация оплаты курса или урока через Stripe",
        description="Генерирует сессию Stripe Checkout и возвращает прямую безопасную ссылку на оплату.",
        responses={201: PaymentSerializer}
    )
)
class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Финтех-контроллер для создания платежа с интеграцией Stripe API (Задание 2).
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Считываем переданные клиентом параметры
        paid_course = serializer.validated_data.get("paid_course")
        paid_lesson = serializer.validated_data.get("paid_lesson")
        amount = serializer.validated_data.get("amount")

        if not paid_course and not paid_lesson:
            raise ValidationError("Необходимо указать ID оплачиваемого курса или урока.")
        if amount <= 0:
            raise ValidationError("Сумма платежа должна быть больше нуля.")

        # 2. Формируем название продукта для Stripe
        product_name = paid_course.name if paid_course else paid_lesson.name

        # 3. Вызываем финтех-цепочку Stripe через сервисный слой (Задание 2)
        stripe_product_id = StripeService.create_stripe_product(product_name)

        # Переводим сумму в копейки: умножаем Decimal на 100 и приводим к целому int (ТЗ критерий)
        amount_in_cents = int(amount * 100)
        stripe_price_id = StripeService.create_stripe_price(amount_in_cents, stripe_product_id)

        # Ссылки возврата (для тестов используем локальные заглушки)
        success_url = "http://127.0.0"
        cancel_url = "http://127.0.0"

        # Генерируем платежную сессию (Задание 2)
        stripe_session_id, stripe_payment_url = StripeService.create_stripe_checkout_session(
            stripe_price_id, success_url, cancel_url
        )

        # 4. Сохраняем все данные в модель, автоматически привязывая авторизованного юзера (Задание 2)
        serializer.save(
            user=self.request.user,
            stripe_session_id=stripe_session_id,
            stripe_payment_url=stripe_payment_url
        )
