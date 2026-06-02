# Бэкенд-платформа онлайн-обучения "LMS-API"

## Описание проекта:
Проект представляет собой специализированный бэкенд-сервер для LMS-системы (Learning Management System), разработанный в рамках концепции SPA (Single Page Application) [config:settings]. Сервер функционирует исключительно в режиме REST API, принимая и отдавая строго структурированные JSON-данные. Платформа построена на базе фреймворка Django с использованием инструментария Django Rest Framework (DRF) и СУБД PostgreSQL [Задание 1, 2].

---

## 📋 Чек-лист проверки функционала (Урок 32.1)

### 1. Архитектура, Сериализаторы и Финансы (Уроки 30.1 - 30.2)
- [ ] **Интеграция DRF и Модели:** К проекту подключен пакет `djangorestframework` [Задание 1]. В приложении `users` развернута модель `User` на базе `AbstractBaseUser` с авторизацией по `email` [users:models]. В приложении `materials` спроектированы сущности **Курс** и **Урок** со связью «один-ко-многим» [materials:models].
- [ ] **Агрегация и Финансы:** В `CourseSerializer` добавлено динамическое поле `lessons_count` (`SerializerMethodField()`) и сквозной вложенный массив `lessons` [materials:serializers]. Создана модель `Payment` для учета оплат с фильтрацией `django-filter` и кастомной командой наполнения `fill_payments` [users:models].

### 2. Авторизация и Разграничение Прав Доступа (Урок 31)
- [ ] **JWT-безопасность:** Интегрирована токенизированная защита `rest_framework_simplejwt` [config:settings]. API закрыт проверкой `IsAuthenticated`.
- [ ] **Ролевая модель:** Спроектирована группа "Модераторы" и кастомный permission-класс `IsModerator` [users:permissions]. Модераторы могут только читать и изменять контент, но лишены прав на создание и удаление [materials:views]. Обычные пользователи через класс `IsOwner` управляют исключительно своими объектами [users:permissions].

### 3. Валидация, Подписки и Пагинация (Урок 32.1)
- [ ] **Валидация контента (Задание 1):** Разработана функция-валидатор `validate_youtube_url` [materials:validators]. Она привязана к полю `video_url` в сериализаторе уроков и блокирует любые внешние ссылки, кроме видеохостинга `youtube.com` / `youtu.be` [materials:serializers]. При ошибке возвращается понятный человекочитаемый JSON-текст.
- [ ] **Модель подписок (Задание 2):** В приложении `materials` создана модель `Subscription` [materials:models]. Гарантирована уникальность пары ID пользователя и ID курса через `UniqueConstraint` базы данных [materials:models].
- [ ] **Управление подписками (Задание 2):** Реализован эндпоинт `courses/subscribe/` на базе `APIView` с методом `POST` [materials:views, materials:urls]. Он удаляет подписку при ее наличии или создает при отсутствии, возвращая корректные сообщения.
- [ ] **Признак подписки в курсах (Задание 2):** В `CourseSerializer` интегрировано динамическое поле `is_subscribed` (`SerializerMethodField`), отображающее статус подписки текущего авторизованного студента на этот курс [materials:serializers].
- [ ] **Пагинация LMS (Задание 3):** Создан класс `LMSPagination` на базе `PageNumberPagination` с параметрами `page_size=5`, `page_size_query_param` и `max_page_size=50` [materials:paginators]. Пагинация успешно добавлена в ViewSet курсов и список уроков [materials:views].

### 4. Автоматизированное тестирование (Задание 4)
- [ ] **Комплексные тесты:** Написаны автоматические тесты в файле `materials/tests.py`, покрывающие полный цикл CRUD для уроков, логику подписок на курсы и проверку ролей доступов (студенты/модераторы) через `force_authenticate()` [materials:tests].
- [ ] **Покрытие кода (Coverage):** Интегрирована утилита `coverage` [config:settings]. Все 9 тестов проходят со статусом `OK`, а итоговый отчет зафиксирован в корневом файле `coverage.txt` с показателем покрытия **83%**.

---

## Стек технологий и окружение:
* **Python** версии 3.13 [config:settings]
* **Django** версии 6.0+ [config:settings]
* **Django Rest Framework** версии 3.15+ [config:settings]
* **Simple-JWT** (JSON Web Token авторизация) [config:settings]
* **Django-filter** (фильтрация API эндпоинтов) [config:settings]
* **Coverage** (анализ покрытия кода тестами) [config:settings]
* **PostgreSQL** (основная СУБД) [config:settings]
* **Пакетный менеджер:** Poetry [config:settings]

---

## Инструкция по установке и запуску:

1. **Установите все зависимости проекта через Poetry:**
   ```bash
   poetry install
   ```
2. **Настройте файл переменных окружения `.env` в корне проекта:**
   ```env
   SECRET_KEY="ваш_уникальный_секретный_ключ"
   DEBUG=True
   DB_NAME=lms_db
   DB_USER=postgres
   DB_PASSWORD=ваш_пароль_от_postgres
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```
3. **Сгенерируйте и примените миграции базы данных:**
   ```bash
   poetry run python manage.py database_sync
   poetry run python manage.py migrate
   ```
4. **Создайте системную группу модераторов и наполните базу платежами:**
   ```bash
   poetry run python manage.py create_moderators
   poetry run python manage.py fill_payments
   ```
5. **Запустите автоматические тесты и проверьте покрытие:**
   ```bash
   poetry run coverage run --source='.' manage.py test
   poetry run coverage report
   ```
6. **Запустите локальный API-сервер:**
   ```bash
   poetry run python manage.py runserver
   ```

---

## Базовые эндпоинты API для тестирования:

* **Регистрация нового студента:** `POST -> 127.0.0.1:8000/api/users/register/`
* **Авторизация (Получение Access/Refresh токенов):** `POST -> 127.0.0.1:8000/api/users/token/`
* **Управление подпиской на курс (Переключатель):** `POST -> 127.0.0.1:8000/api/courses/subscribe/` (Передать JSON `{"course_id": <id>}`)
* **Пагинированный список курсов (с признаком подписки):** `GET -> 127.0.0.1:8000/api/courses/`
* **Пагинированный список уроков:** `GET -> 127.0.0.1:8000/api/lessons/`
