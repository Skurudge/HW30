import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Читаем конфигурацию из settings.py с префиксом CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически ищем задачи (tasks.py) во всех зарегистрированных приложениях
app.autodiscover_tasks()

# Настройка расписания Celery Beat (Задание 1, 3)
app.conf.beat_schedule = {
    "block-inactive-users-every-day": {
        "task": "users.tasks.check_inactive_users",
        "schedule": crontab(hour="0", minute="0"),
    },
}
