import stripe
from django.conf import settings
from rest_framework.exceptions import APIException

# Инициализируем секретный ключ Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Сервисный слой для интеграции с платежным шлюзом Stripe API (Задание 2)."""

    @staticmethod
    def create_stripe_product(name: str) -> str:
        """Создает продукт в системе Stripe и возвращает его уникальный ID (Задание 2)."""
        try:
            product = stripe.Product.create(name=name)
            return product.id
        except stripe.error.StripeError as e:
            raise APIException(f"Ошибка Stripe при создании продукта: {str(e)}")

    @staticmethod
    def create_stripe_price(amount: int, product_id: str) -> str:
        """
        Создает цену для продукта в системе Stripe и возвращает её ID (Задание 2).
        Сумма amount передается в копейках (ТЗ критерий оценки).
        """
        try:
            price = stripe.Price.create(
                currency="rub",
                unit_amount=amount,  # Цена в копейках (например, 1500 руб = 150000 копеек)
                product=product_id,
            )
            return price.id
        except stripe.error.StripeError as e:
            raise APIException(f"Ошибка Stripe при формировании цены: {str(e)}")

    @staticmethod
    def create_stripe_checkout_session(price_id: str, success_url: str, cancel_url: str) -> tuple[str, str]:
        """
        Создает безопасную платежную сессию и возвращает кортеж (session_id, payment_url) (Задание 2).
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return session.id, session.url
        except stripe.error.StripeError as e:
            raise APIException(f"Ошибка Stripe при генерации платежной сессии: {str(e)}")
