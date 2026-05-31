from decimal import Decimal
from django.core.management.base import BaseCommand
from users.models import User, Payment
from materials.models import Course, Lesson


class Command(BaseCommand):
    """Кастомная команда для наполнения БД тестовыми платежами (Задание 2)."""
    help = "Наполнение базы данных тестовыми курсами, уроками, пользователями и платежами"

    def handle(self, *args, **options):
        # 1. Очищаем старые платежи, чтобы избежать дублирования
        Payment.objects.all().delete()

        # 2. Создаем или получаем тестового пользователя
        user, created = User.objects.get_or_create(
            email="student@example.com",
            defaults={"city": "Москва", "phone": "+79991112233"}
        )
        if created:
            user.set_password("lms_password_2026")
            user.save()

        # 3. Создаем базовый курс и урок, если их нет
        course, _ = Course.objects.get_or_create(
            name="Веб-разработка на Python",
            defaults={"description": "Профессиональный курс по Django и FastAPI"}
        )

        lesson, _ = Lesson.objects.get_or_create(
            name="Введение в DRF и Сериализаторы",
            course=course,
            defaults={"description": "Основы проектирования REST API", "video_url": "https://youtube.com"}
        )

        # 4. Записываем тестовые платежи согласно ТЗ
        Payment.objects.create(
            user=user,
            paid_course=course,
            amount=Decimal("45000.00"),
            payment_method=Payment.PAYMENT_METHOD_TRANSFER
        )

        Payment.objects.create(
            user=user,
            paid_lesson=lesson,
            amount=Decimal("1500.00"),
            payment_method=Payment.PAYMENT_METHOD_CASH
        )

        self.stdout.write(self.style.SUCCESS("Таблицы LMS успешно наполнены тестовыми данными!"))
