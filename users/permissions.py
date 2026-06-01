from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Кастомный класс проверки прав для группы 'Модераторы' (Задание 2).
    Разрешает доступ на чтение и изменение, если пользователь в группе модераторов.
    """

    def has_permission(self, request, view):
        # Проверяем, авторизован ли пользователь и состоит ли он в группе Модераторы
        if request.user.is_authenticated:
            return request.user.groups.filter(name="Модераторы").exists()
        return False


class IsOwner(permissions.BasePermission):
    """
    Кастомный класс проверки прав на уровне конкретного объекта (Задание 3).
    Разрешает доступ только непосредственному создателю (владельцу) записи.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем равенство авторизованного пользователя и поля owner у модели
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        return False
