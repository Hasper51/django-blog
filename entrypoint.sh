#!/bin/bash

set -e  # Завершить выполнение при ошибке
set -u  # Завершить выполнение при обращении к несуществующей переменной

# Функция для ожидания доступности порта
wait_for_port() {
    local host="$1"
    local port="$2"
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if pg_isready -h "$host" -p "$port" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" >/dev/null 2>&1; then
            echo "PostgreSQL на $host:$port готов к работе!"
            return 0
        fi

        echo "Попытка $attempt из $max_attempts: Ожидание PostgreSQL на $host:$port..."
        attempt=$((attempt + 1))
        sleep 2
    done

    echo "Ошибка: PostgreSQL не стал доступен после $max_attempts попыток."
    return 1
}

# Проверка доступности PostgreSQL
POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

echo "Начинаем проверку доступности PostgreSQL..."
wait_for_port "$POSTGRES_HOST" "$POSTGRES_PORT"

echo "Запуск Django приложения..."
exec python manage.py runserver 0.0.0.0:8000
