# Используем официальный легковесный образ Python
FROM python:3.13-slim

# Устанавливаем системные зависимости для сборки psycopg2 и работы с сетью
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем Poetry напрямую через pip — быстро, надежно и без ошибок окружения!
RUN pip install --no-cache-dir poetry

# Отключаем создание виртуальных окружений внутри контейнера, ставим пакеты прямо в систему
RUN poetry config virtualenvs.create false

# Копируем файлы зависимостей проекта
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости без режима сборки самого пакета lms
RUN poetry install --no-root

# Копируем весь остальной код проекта в контейнер
COPY . .

# Открываем порт для Django-сервера
EXPOSE 8000
