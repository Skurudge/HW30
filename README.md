# Бэкенд-платформа онлайн-обучения "LMS-API"

## Описание проекта:
Проект представляет собой специализированный бэкенд-сервер для LMS-системы (Learning Management System), разработанный в рамках концепции SPA (Single Page Application) [config:settings]. Сервер функционирует исключительно в режиме REST API, принимая и отдавая строго структурированные JSON-данные. Платформа построена на базе фреймворка Django с использованием инструментария Django Rest Framework (DRF) и СУБД PostgreSQL [Задание 1, 2].

---

## 📋 Чек-лист проверки функционала (Урок 32.2)

### 1. Архитектура, Сериализаторы и Финансы (Уроки 30.1 - 30.2)
- [ ] **1. Интеграция DRF:** К проекту подключен пакет `djangorestframework` [Задание 1].
- [ ] **2. Кастомная модель пользователя:** В приложении `users` развернута модель `User` на базе `AbstractBaseUser` с авторизацией по `email` [users:models]. Добавлены профильные поля: телефон, город и аватарка.
- [ ] **3. Модели материалов обучения:** В приложении `materials` спроектированы сущности **Курс** и **Урок** со связью «один-ко-многим» [materials:models].
- [ ] **4. CRUD для Курсов и Уроков:** С помощью `ModelViewSet` развернут полный автоматический набор API-эндпоинтов для курсов [materials:views]. На базе цепочки Generic-классов вручную описаны изолированные эндпоинты для всех операций с уроками.
- [ ] **5. Подсчет уроков:** В `CourseSerializer` добавлено динамическое поле `lessons_count` (`SerializerMethodField()`) [materials:serializers].
- [ ] **6. Вложенная структура:** Реализован сквозной вывод уроков внутри курса (массив `lessons` в JSON) [materials:serializers].
- [ ] **7. Первичная модель платежей:** Создана модель `Payment` для учета базовых оплат с фильтрацией `django-filter` и кастомной командой наполнения `fill_payments` [users:models, users:management:commands:fill_payments].

### 2. Авторизация и Разграничение Правы Доступа (Урок 31)
- [ ] **8. JWT-безопасность:** Интегрирована токенизированная защита `rest_framework_simplejwt` [config:settings]. Глобальный API закрыт проверкой `IsAuthenticated`.
- [ ] **9. Открытая регистрация:** Разработан открытый эндпоинт `users/register/` с правами `AllowAny` [users:views, users:urls]. Пароли принудительно хэшируются (`set_password`).
- [ ] **10. Модераторский доступ:** Спроектирована группа "Модераторы" и кастомный permission-класс `IsModerator` [users:permissions]. Модераторы могут только читать и изменять контент, но лишены прав на создание и удаление [materials:views].
- [ ] **11. Права владельцев:** Обычные пользователи через класс `IsOwner` управляют исключительно своими объектами [users:permissions]. Настроен автоматический хук `perform_create` [materials:views].
- [ ] **12. Защита чужих профилей:** При просмотре чужого аккаунта пароль и история оплат автоматически скрываются из JSON-выдачи [users:serializers].

### 3. Валидация, Подписки и Тестирование (Урок 32.1)
- [ ] **13. Валидация контента:** Разработана функция-валидатор `validate_youtube_url`, блокирующая любые внешние видео-ссылки в уроках, кроме `youtube.com` / `youtu.be` [materials:validators].
- [ ] **14. Модель и управление подписками:** Реализован эндпоинт `courses/subscribe/` с логикой `UniqueConstraint` базы данных для переключения статуса подписки студента на курс [materials:views, materials:models]. Status-признак `is_subscribed` выводится в курсах [materials:serializers].
- [ ] **15. Пагинация LMS:** Создан класс `LMSPagination` (`page_size=5`), ограничивающий постраничный вывод списков курсов и уроков [materials:paginators, materials:views].
- [ ] **16. Автоматизированное тестирование:** Написаны 9 комплексных тестов в `materials/tests.py`, проверяющих CRUD, роли и подписки [materials:tests]. Итоговый отчет зафиксирован в файле `coverage.txt` с покрытием кода **83%**.

### 4. Документирование и Безопасность (Урок 32.2)
- [ ] **17. Автодокументирование Swagger & Redoc (Задание 1):** Интегрирован генератор схем OpenAPI 3 через `drf-spectacular` [config:settings]. Интерактивная документация параметров, схем запросов и ошибок доступна по адресам `api/docs/swagger/` и `api/docs/redoc/` [config:urls]. Нестандартные контроллеры описаны вручную через `@extend_schema` [users:views].
- [ ] **18. Финтех-интеграция Stripe API (Задание 2):** Реализован сервисный слой `StripeService` с перехватом исключений [materials:services]. Контроллер `PaymentCreateAPIView` регистрирует продукты, переводит суммы строго в копейки (`int`), генерирует сессии Checkout и возвращает клиенту прямую ссылку на оплату [users:views].
- [ ] **19. Проверка статуса сессии (Дополнительное задание):** Реализован эндпоинт проверки статуса транзакции по её ID. Контроллер обращается к Stripe методом Retrieve (`Session.retrieve`) и отдает актуальный статус оплаты (`payment_status`) в JSON-формате [users:views, users:urls].

---

## Стек технологий и окружение:
* **Python** версии 3.13 [config:settings]
* **Django** версии 6.0+ [config:settings]
* **Django Rest Framework** версии 3.15+ [config:settings]
* **Simple-JWT** (JSON Web Token авторизация) [config:settings]
* **Stripe API SDK** (финтех-интеграция эквайринга) [config:settings]
* **Drf-spectacular** (документация OpenAPI 3 Swagger/Redoc) [config:settings]
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
   STRIPE_SECRET_KEY="ваш_секретный_тестовый_ключ_stripe_sk_test_..."
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
5. **Запустите локальный API-сервер:**
   ```bash
   poetry run python manage.py runserver
   ```

---

## Финтех-эндпоинты API для тестирования в Postman:

* **Инициация покупки курса/урока в Stripe:** `POST -> 127.0.0.1:8000/api/users/payments/create/` (Передать JSON `{"paid_course": 1, "amount": 2500.00}`)
* **Проверка актуального статуса оплаты транзакции в Stripe:** `GET -> 127.0.0.1:8000/api/users/payments/<id_платежа>/status/`
* **Интерактивная документация Swagger UI:** `GET -> 127.0.0.1:8000/api/docs/swagger/`
