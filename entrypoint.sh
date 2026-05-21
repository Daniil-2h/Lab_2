#!/bin/bash
echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Выполняем миграции
alembic upgrade head

# Запускаем приложение
exec uvicorn app.main:app --host 0.0.0.0 --port 4200