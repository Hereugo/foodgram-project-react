# Foodgram (Продуктовый помощник)

![Badge Status](https://github.com/Hereugo/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg) 

Текущий роботающия проект доступен по адресу http://51.250.103.68/

## Администраторский аккаунт
Логин: admin
Пароль: admin

## Описание

Продуктовый помощник Foodgram позволяет пользователям публиковать рецепты, добавлять понравившиеся рецепты в избранное и подписываться на публикации других авторов. Также есть возможность скачать список продуктов, необходимых для приготовления выбранных блюд.

## Автор

Амир Нурмухамбетов ([github profile](https://github.com/Hereugo))

## Технологии

- Python 3.8
- Django 2.2.28
- DRF (Django Rest Framework)
- PostgreSQL
- Docker Compose
- Nginx
- Gunicorn

## Шаблон наполнения env-файла 

``` 
SECRET_KEY=your_secret_key 
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=your_db_name 
POSTGRES_USER=your_db_user 
POSTGRES_PASSWORD=your_db_password 
DB_HOST=db 
DB_PORT=5432 
``` 

## Установка на Докере

1. Склонируйте репозиторий на свой компьютер

```bash
git clone git@github.com:Hereugo/foodgram-project-react.git
```

2. Перейдите в папку с проектом

```bash
cd foodgram-project-react
cd infra
```

3. Создайте файл .env и заполните его переменными окружения

```bash
touch .env
```

4. Запустите проект

```bash
docker-compose up -d --build
```

5. Перейдите в контейнер с проектом

```bash
docker-compose exec backend bash
```

6. Выполните миграции

```bash
python manage.py migrate
```

7. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

8. Соберите статику

```bash
python manage.py collectstatic
```

9. Загрузите фикстуры для ингредиентов

```bash
python manage.py load_data
```

10. Перейти по адресу http://localhost 

## API документация

Документация доступна по адресу http://localhost/redoc
