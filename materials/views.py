from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для реализации полного CRUD Курса с разделением прав по action (Задание 2, 3).
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        """Автоматическая привязка создаваемого курса к текущему пользователю (Задание 3)."""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Динамическое распределение прав в зависимости от операции (Задание 2, 3)."""
        if self.action == "create":
            # Модераторы не могут создавать курсы (Задание 2)
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update"]:
            # Редактировать могут либо модераторы, либо владельцы (Задание 2, 3)
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            # Удалять могут только владельцы, модераторам запрещено (Задание 2, 3)
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            # Просматривать список и детали могут либо модераторы, либо владельцы (Задание 2, 3)
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Модераторы видят всё, обычные пользователи — только своё (Задание 2, 3)."""
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)


# --- Набор Generic-классов для реализации CRUD Уроков (Задание 2, 3) ---

class LessonCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания урока. Запрещен модераторам (Задание 2, 3)."""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """Автоматическая привязка создаваемого урока к текущему пользователю (Задание 3)."""
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Эндпоинт получения списка уроков. Фильтруется по роли (Задание 2, 3)."""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра урока. Доступен модераторам или владельцам (Задание 2, 3)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт редактирования урока. Доступен модераторам или владельцам (Задание 2, 3)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления урока. Запрещен модераторам, доступен только владельцу (Задание 2, 3)."""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
