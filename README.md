
## Проект Foodhelper
### Описание проекта

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


## 🛠 Технологии:
- **Python 3.9**
- **Django 3.2**
- **Gunicorn**
- **PostgreSQL**

![workflow badge](https://github.com/makhotin07/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Как запустить проект:

Для запуска проекта на локальной машине у вас должен быть установлен Docker.
Клонируйте репозиторий:
```
git clone git@github.com:nucluster/foodgram-project-react.git
```

Измените свою текущую рабочую директорию:
```
cd infra
```

Создайте .env файл следущего содержания:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
``` 
Все последующие команды выполняются с правами суперпользователя 
или члена группы docker (см. документацию Docker) 

Выполните команду:
```
docker compose up -d --build
```

Соберите статику:
```
docker compose exec backend python manage.py collectstatic --no-input
```
Создайте файлы миграций:
```
docker compose exec backend python manage.py makemigrations 
```

Примените миграции:
```
docker compose exec backend python manage.py migrate
```

Создайте суперпользователя Django:
```
docker compose exec backend python manage.py createsuperuser
```

Для загрузки данных из csv файлов:
```
docker compose exec backend python manage.py import_csv
```


**Над проектом работал:** [Мишков Андрей](https://github.com/MartiAndrew)