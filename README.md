
# Проект Foodhelper

***

### Описание проекта:
Cайт Foodhelper («Помощник подбора продуктов»).   
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.



## Основные возможности проекта
- Создание пользователей сайта;
- Просмотр списка рецептов;
- Создание, удаление и редактировани рецептов;
- Добавление рецептов в избранное;
- Добавления рецептов в список покупок;
- Возможность подписки на других авторов;
- Получение списка необходимых к покупке ингредиентов в виде txt-файла.


## Технологии:
- **Python 3.9**
- **Django 3.2**
- **Django Rest Framework 3.14**
- **Gunicorn**
- **PostgreSQL**

![CI](https://img.shields.io/badge/Django%20Rest%20Framework-3.14-success)
![CI](https://img.shields.io/badge/Django-3.2-green)
![CI](https://img.shields.io/badge/Python-v3.9-blue)
![CI](https://img.shields.io/badge/-Djoser-yellowgreen)
![CI](https://img.shields.io/badge/-Nginx-blueviolet)
![CI](https://img.shields.io/badge/-Docker-blueviolet)
![CI](https://img.shields.io/badge/-Linux-red)

***

## Как запустить проект:

Для запуска проекта на локальной машине у вас должен быть установлен Docker.
*Устанавливаем Docker и Docker compose:*
```python
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
*Устанавливаем разрешение для docker compose*
```python
sudo chmod +x /usr/local/bin/docker-compose
```
*Клонируйте репозиторий:*
```
git clone git@github.com:nucluster/foodgram-project-react.git
```

*Измените свою текущую рабочую директорию:*
```
cd infra
```

*Создайте .env файл следущего содержания:*
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
``` 
Все последующие команды выполняются с правами суперпользователя  

*Выполните команду:*
```
docker compose up -d --build
```

*Соберите статику:*
```
docker compose exec backend python manage.py collectstatic --no-input
```
*Создайте файлы миграций:*
```
docker compose exec backend python manage.py makemigrations 
```

*Примените миграции:*
```
docker compose exec backend python manage.py migrate
```

*Создайте суперпользователя Django:*
```
docker compose exec backend python manage.py createsuperuser
```

*Для загрузки данных из csv файлов:*
```
docker compose exec backend python manage.py import_csv
```

***

**Над проектом работал:** [Мишков Андрей](https://github.com/MartiAndrew)