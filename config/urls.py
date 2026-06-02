from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)  # Импорт схемы автодокументирования (Задание 1)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Маршруты приложений
    path("api/", include("materials.urls", namespace="materials")),
    path("api/users/", include("users.urls", namespace="users")),

    # Эндпоинты автогенерации документации OpenAPI 3 / Swagger (Задание 1)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
