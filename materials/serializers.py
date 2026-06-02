from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Урока с валидатором на поле видео-ссылки (Задание 1, 3)."""

    # Привязываем валидатор напрямую к конкретному полю по ТЗ
    video_url = serializers.URLField(validators=[validate_youtube_url], required=False, allow_blank=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса со сквозным выводом уроков и признаком подписки (Задание 2, 3)."""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "name", "preview", "description", "lessons_count", "is_subscribed", "lessons")

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False
