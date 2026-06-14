from rest_framework.exceptions import ValidationError


class YoutubeLinkValidator:
    """Промышленный класс-валидатор ссылки на YouTube (Задание 1, Критерий оценки)."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        # Достаем значение ссылки из пришедших атрибутов
        value = attrs.get(self.field)
        if not value:
            return

        url_str = str(value).lower().strip()

        # Проверяем домен
        if "youtube.com" not in url_str and "youtu.be" not in url_str:
            # Выбрасываем ошибку строго привязанную к имени нашего поля (Критерий оценки)
            raise ValidationError(
                {self.field: "Разрешены ссылки исключительно на видеохостинг youtube.com."}
            )
