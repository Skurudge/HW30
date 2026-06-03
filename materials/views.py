from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer
from materials.paginators import LMSPagination
from materials.tasks import send_course_update_email  # Импортируем нашу задачу (Задание 2)
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для управления курсами с интеграцией пагинации и асинхронных задач (Задание 2, 3)."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LMSPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Интеллектуальный триггер рассылки при обновлении КУРСА (Задание 2, Доп. задание)."""
        course = serializer.save()

        # Получаем время предыдущего изменения до текущего сохранения
        # (Используем небольшую дельту в 5 секунд, так как auto_now обновил поле в базе прямо сейчас)
        threshold_time = timezone.now() - timedelta(hours=4)

        # Дополнительное задание: Уведомление улетает, только если курс не обновлялся более 4 часов
        if course.updated_at < threshold_time:
            # Вызываем асинхронную задачу Celery (Задание 2)
            send_course_update_email.delay(course.id)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists() or self.action == "retrieve":
            return Course.objects.all()
        return Course.objects.filter(owner=user)


# --- Набор Generic-классов для реализации CRUD Уроков ---

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = LMSPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер изменения урока с триггером фонового обновления курса (Задание 2, Доп. задание)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        course = lesson.course

        threshold_time = timezone.now() - timedelta(hours=4)

        # Обновление урока — это обновление материалов курса. Проверяем 4-часовой интервал курса
        if course.updated_at < threshold_time:
            send_course_update_email.delay(course.id)

        # Принудительно сохраняем сам курс, чтобы обновить его собственный таймстемп updated_at
        course.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена."
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена."

        return Response({"message": message})
