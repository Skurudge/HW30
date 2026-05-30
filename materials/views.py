from rest_framework import viewsets, generics
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для реализации полного CRUD для модели Курса (Задание 3)."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# --- Набор Generic-классов для реализации CRUD Уроков (Задание 3) ---

class LessonCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания урока."""
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """Эндпоинт для получения списка уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт для просмотра конкретного урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт для редактирования (обновления) урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления урока."""
    queryset = Lesson.objects.all()
