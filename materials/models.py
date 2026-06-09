from django.db import models
from django.conf import settings

class Course(models.Model):
    """Модель курса платформы онлайн-обучения."""
    title = models.CharField(max_length=150, verbose_name="Название курса")
    preview = models.ImageField(upload_to="materials/courses/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Владелец",
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __init__(self, *args, **kwargs):
        # Если тест или сериализатор передает 'name', прозрачно перекидываем в 'title'
        if 'name' in kwargs:
            kwargs['title'] = kwargs.pop('name')
        super().__init__(*args, **kwargs)

    @property
    def name(self):
        return self.title

    @name.setter
    def name(self, value):
        self.title = value

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока платформы онлайн-обучения."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    title = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    preview = models.ImageField(upload_to="materials/lessons/", blank=True, null=True, verbose_name="Превью")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __init__(self, *args, **kwargs):
        # Если тест или сериализатор передает 'name', прозрачно перекидываем в 'title'
        if 'name' in kwargs:
            kwargs['title'] = kwargs.pop('name')
        super().__init__(*args, **kwargs)

    @property
    def name(self):
        return self.title

    @name.setter
    def name(self, value):
        self.title = value

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """Модель подписки пользователя на обновления курса."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.email} -> {self.course.title}"
