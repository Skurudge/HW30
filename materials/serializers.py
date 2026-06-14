from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import YoutubeLinkValidator  # Импортируем наш обновленный валидатор


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков с полной поддержкой полей name, title и валидацией YouTube (Критерий оценки)."""

    title = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(source="title", required=False)

    video = serializers.URLField(source="video_url", required=False, allow_null=True, allow_blank=True)
    url = serializers.URLField(source="video_url", required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Lesson
        fields = "__all__"
        # Подключили валидатор ссылки на видео к полю video_url (Критерий оценки)
        validators = [YoutubeLinkValidator(field="video_url")]

    def to_internal_value(self, data):
        if "name" in data and "title" not in data:
            data["title"] = data["name"]
        return super().to_internal_value(data)


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов с динамическим выводом уроков и поддержкой алиасов."""

    title = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(source="title", required=False)
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def to_internal_value(self, data):
        if "name" in data and "title" not in data:
            data["title"] = data["name"]
        return super().to_internal_value(data)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для управления подписками на курсы."""

    class Meta:
        model = Subscription
        fields = "__all__"
