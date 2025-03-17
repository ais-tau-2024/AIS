#!/bin/bash

# Проверяем, существует ли виртуальное окружение
if [ ! -d "venv" ]; then
    echo "Ошибка: Виртуальное окружение 'venv' не найдено!"
    exit 1
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Запускаем сервер Django
python manage.py runserver
