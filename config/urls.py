from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Подключаем API-эндпоинты наших приложений
    path("api/", include("materials.urls", namespace="materials")),
    path("api/users/", include("users.urls", namespace="users")),
]

# Раздача медиафайлов (картинок) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
