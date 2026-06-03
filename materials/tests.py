from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from materials.models import Course, Lesson, Subscription


class LMSTestCase(APITestCase):
    """Комплексное тестирование CRUD уроков, подписок и ролевой модели доступа (Задание 4)."""

    def setUp(self):
        """Заполнение базы данных тестовыми сущностями перед каждым тестом (Задание 4)."""
        # Создаем тестовые группы
        self.moderator_group, _ = Group.objects.get_or_create(name="Модераторы")

        # Создаем пользователей
        self.user_owner = User.objects.create_user(email="owner@test.com", password="password123")
        self.user_moderator = User.objects.create_user(email="moder@test.com", password="password123")
        self.user_moderator.groups.add(self.moderator_group)
        self.user_other = User.objects.create_user(email="other@test.com", password="password123")

        # Создаем базовый курс и урок
        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание курса",
            owner=self.user_owner
        )
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            description="Описание урока",
            video_url="https://youtube.com",
            course=self.course,
            owner=self.user_owner
        )

    # ==================== ТЕСТИРОВАНИЕ CRUD УРОКОВ (Задание 4) ====================

    def test_create_lesson_success(self):
        """Успешное создание урока владельцем с валидной ссылкой YouTube (Задание 1, 4)."""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("materials:lesson_create")
        data = {
            "name": "Новый урок",
            "description": "Свежее описание",
            "video_url": "https://youtube.com",
            "course": self.course.id
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.filter(name="Новый урок").count(), 1)
        self.assertEqual(Lesson.objects.get(name="Новый урок").owner, self.user_owner)

    def test_create_lesson_validation_error(self):
        """Ошибка создания урока при передаче запрещенной сторонней ссылки (Задание 1, 4)."""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("materials:lesson_create")
        data = {
            "name": "Запрещенный урок",
            "video_url": "https://wikipedia.org",  # Ссылка не на youtube
            "course": self.course.id
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("video_url", response.data)
        self.assertEqual(
            response.data["video_url"][0],
            "Разрешены ссылки исключительно на видеохостинг youtube.com."
        )

    def test_create_lesson_moderator_denied(self):
        """Проверка ограничения доступов: модератор не может создавать уроки (Задание 2, 4)."""
        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("materials:lesson_create")
        data = {"name": "Урок модератора", "course": self.course.id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lessons_list(self):
        """Получение списка уроков с проверкой пагинации (Задание 3, 4)."""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("materials:lesson_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Так как пагинатор возвращает структуру {'results': [...]}, проверяем наличие ключа
        self.assertIn("results", response.data)

    def test_retrieve_lesson_owner_and_moderator(self):
        """Просмотр деталей урока разрешен как владельцу, так и модератору (Задание 2, 3)."""
        url = reverse("materials:lesson_detail", kwargs={"pk": self.lesson.pk})

        # Проверяет владелец
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяет модератор
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяет посторонний студент — доступ должен быть закрыт
        self.client.force_authenticate(user=self.user_other)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson(self):
        """Редактирование урока разрешено владельцу и модератору (Задание 2, 3, 4)."""
        url = reverse("materials:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"name": "Обновленное имя"}

        # Обновляет модератор
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Обновляет владелец
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.patch(url, {"name": "Имя от владельца"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_moderator_denied(self):
        """Модератор не имеет права удалять уроки (Задание 2, 4)."""
        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("materials:lesson_delete", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_owner_success(self):
        """Владелец может беспрепятственно удалить свой урок (Задание 3, 4)."""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("materials:lesson_delete", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.filter(pk=self.lesson.pk).count(), 0)

    # ==================== ТЕСТИРОВАНИЕ ПОДПИСОК (Задание 4) ====================

    def test_toggle_subscription_flow(self):
        """Тест полного цикла подписки: создание при отсутствии, удаление при наличии (Задание 2, 4)."""
        self.client.force_authenticate(user=self.user_other)
        url = reverse("materials:course_subscribe")
        data = {"course_id": self.course.id}

        # 1. Первая попытка — подписки нет, она должна создаться
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена.")
        self.assertTrue(Subscription.objects.filter(user=self.user_other, course=self.course).exists())

        # Проверяем, что в сериализаторе курса признак подписки стал True (Задание 2)
        course_url = reverse("materials:courses-detail", kwargs={"pk": self.course.pk})
        course_response = self.client.get(course_url)
        self.assertEqual(course_response.data["is_subscribed"], True)

        # 2. Вторая попытка — подписка уже существует, она должна удалиться
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена.")
        self.assertFalse(Subscription.objects.filter(user=self.user_other, course=self.course).exists())
