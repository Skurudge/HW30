from rest_framework.exceptions import ValidationError


def validate_youtube_url(value):
    """Функция-валидатор для проверки ссылки на видео (Задание 1)."""
    if not value:
        return

    url_str = str(value).lower().strip()

    # Проверяем, содержит ли ссылка разрешенные домены
    if "youtube.com" not in url_str and "youtu.be" not in url_str:
        raise ValidationError("Разрешены ссылки исключительно на видеохостинг youtube.com.")
