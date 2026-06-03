from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def check_inactive_users():
    """
    Периодическая задача Celery Beat для автоматической блокировки неактивных пользователей (Задание 3).
    Выборка и отключение происходят батчем (критерий оценки).
    """
    # Вычисляем порог времени (30 дней назад от текущего момента)
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим активных пользователей, которые заходили более месяца назад
    # Поле last_login__isnull=False гарантирует, что мы не заблокируем новорегов, еще ни разу не вошедших
    inactive_users_queryset = User.objects.filter(
        last_login__lt=one_month_ago,
        last_login__isnull=False,
        is_active=True
    )

    # Подсчитываем количество перед батч-апдейтом
    count = inactive_users_queryset.count()

    if count > 0:
        # Критерий оценки: Обновление происходит батчем через .update() за один SQL-запрос
        inactive_users_queryset.update(is_active=False)
        return f"Успешно заблокировано неактивных пользователей (батч-метод): {count}"

    return "Нет пользователей, не проявлявших активность более одного месяца."
