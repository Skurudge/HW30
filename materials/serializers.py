from rest_framework import serializers
from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Урока (Задание 3)."""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Курса (Задание 1, 3)."""

    # Задание 1: Поле для подсчета количества уроков курса
    lessons_count = serializers.SerializerMethodField()

    # Задание 3: Вложенный вывод всех уроков, связанных с этим курсом
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "name", "preview", "description", "lessons_count", "lessons")

    def get_lessons_count(self, obj):
        """Метод подсчета количества уроков для SerializerMethodField (Задание 1)."""
        return obj.lessons.count()
