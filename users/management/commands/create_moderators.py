from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from materials.models import Course, Lesson


class Command(BaseCommand):
    """Кастомная команда для создания группы Модераторы с базовыми правами (Задание 2)."""
    help = "Создание группы 'Модераторы' и назначение ей прав на просмотр и изменение курсов и уроков"

    def handle(self, *args, **options):
        # Создаем или получаем группу Модераторы
        moderator_group, created = Group.objects.get_or_create(name="Модераторы")

        # Получаем типы контента для Курса и Урока
        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        # Отбираем только права на просмотр и изменение согласно ТЗ (без создания и удаления)
        permissions = [
            Permission.objects.get(codename="view_course", content_type=course_content_type),
            Permission.objects.get(codename="change_course", content_type=course_content_type),
            Permission.objects.get(codename="view_lesson", content_type=lesson_content_type),
            Permission.objects.get(codename="change_lesson", content_type=lesson_content_type),
        ]

        # Привязываем права к группе
        moderator_group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Модераторы' создана с правами просмотра и изменения!"))
        else:
            self.stdout.write(self.style.WARNING("Группа 'Модераторы' существует. Права доступа обновлены."))
