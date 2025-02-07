# AIS

## Создание виртуального окружения и установка всех пакетов

### Для Linux

```bash
# Создание и активация виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка Django и необходимых пакетов
pip install --upgrade pip
pip install Django djangorestframework django-cors-headers drf-yasg django-filebrowser django-grappelli pillow
```

### Для Windows

```bash
:: Создание и активация виртуального окружения
python -m venv venv
call venv\Scripts\activate.bat

:: Установка Django и необходимых пакетов
pip install --upgrade pip
pip install Django djangorestframework django-cors-headers drf-yasg django-filebrowser django-grappelli pillow
```

### Команды остальные

```
(запуск сервера) python manage.py runserver

```

### Суперпользователь для входа в админ панель

- username: admin
- password: admin
