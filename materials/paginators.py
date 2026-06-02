from rest_framework.pagination import PageNumberPagination


class LMSPagination(PageNumberPagination):
    """Кастомный пагинатор для курсов и уроков (Задание 3)."""
    page_size = 5  # Количество элементов на одной странице по умолчанию
    page_size_query_param = 'per_page'  # Позволяет клиенту передать ?per_page=10
    max_page_size = 50  # Максимально разрешенный лимит для ввода клиентом
