# Barter Project

Django-приложение для обмена товарами/услугами.

## Установка

1. Клонируйте репозиторий:
   git clone https://github.com/Almadover/barter_project

2. Перейдите в директорию проекта:
   cd barter_project

3. Создайте и активируйте виртуальное окружение:
   python -m venv venv  
   source venv/bin/activate  (Linux/Mac)  
   venv\Scripts\activate     (Windows)

4. Установите зависимости:
   pip install -r requirements.txt

## Миграции

1. Выполните миграции:
   python manage.py migrate

2. (Опционально) Создайте суперпользователя для доступа к админке:
   python manage.py createsuperuser

## Запуск сервера

Запустите сервер разработки:
   python manage.py runserver

Проект будет доступен по адресу http://127.0.0.1:8000/

## Структура проекта

- barter/ – основное Django-приложение (models, views, templates, и т.д.)
- barter_project/ – настройки проекта
- requirements.txt – список зависимостей

## Запуск тестов

Для запуска всех тестов приложения выполните:
   pytest

## База данных

Проект разработан для работы с базой данных PostgreSQL

## Дополнительная информация

- Шаблоны HTML находятся в barter/templates/
- URL конфигурация приложения — barter/urls.py
- Основные настройки — barter_project/settings.py