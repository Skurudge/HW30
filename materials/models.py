from django.db import models
from django.conf import settings


class Course(models.Model):
    """Модель курса обучения с привязкой к владельцу (Задание 2, 3)."""

    name = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/courses/",
        blank=True,
        null=True,
        verbose_name="Превью (картинка)",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    # Поле владельца сущности для Задания 3
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока, связанная с курсом и владельцем (Задание 2, 3)."""

    name = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    preview = models.ImageField(
        upload_to="materials/lessons/",
        blank=True,
        null=True,
        verbose_name="Превью (картинка)",
    )
    video_url = models.URLField(
        blank=True, null=True, verbose_name="Ссылка на видео"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )

    # Поле владельца сущности для Задания 3
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Владелец",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
