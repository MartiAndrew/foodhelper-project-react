
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


## Технологии использованные в проекте:
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
## Схема API-проекта:
 
[Схема API](docs/openapi-schema.yml) - Это схема API проекта.

***

## Как запустить проект локально:

Для запуска проекта на локальной машине у вас должен быть установлен Docker.
- *Устанавливаем Docker и Docker compose:*
```python
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- *Устанавливаем разрешение для docker compose*
```python
sudo chmod +x /usr/local/bin/docker-compose
```
- *Клонируйте репозиторий:*
```
git clone git@github.com:MartiAndrew/foodgram-project-react.git
```

- *Создайте .env файл в корне проекта. Его содержание в файле env.example, который находится в корне проекта.*

Все последующие команды выполняются с правами суперпользователя  

- *Выполните команду:*
```
docker compose up -d --build
```

- *Соберите статику:*
```
docker compose exec backend python manage.py collectstatic --no-input
```
- *Создайте файлы миграций:*
```
docker compose exec backend python manage.py makemigrations 
```

- *Примените миграции:*
```
docker compose exec backend python manage.py migrate
```

- *Создайте суперпользователя Django:*
```
docker compose exec backend python manage.py createsuperuser
```

- *Для загрузки данных из csv файлов:*
```
docker compose exec backend python manage.py import_csv
```

***
## Как запустить проект на сервере:

- *Клонируйте репозиторий:*
```
git clone git@github.com:MartiAndrew/foodgram-project-react.git
```

- *Соединяемся с сервером:*
```makefile
ssh -i ~/.ssh/<путь до вашего закрытого ключа> <имя пользователя на сервере>@<ip-сервера>
```
- *Устанавливаем Docker и Docker compose:*
```python
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- *Устанавливаем разрешение для docker compose*
```python
sudo chmod +x /usr/local/bin/docker-compose
```

- *Создаём домашнюю директорию проекта. Далее создаём .env файл в корне проекта. Его содержание в файле env.example, который находится в корне проекта.*
```text
mkdir foodhelper && cd foodhelper/
touch .env
```

- *находясь на локальном компьютере в корневой директории скаченного проекта зайдите в папку infra и выполните команду копирования её содержимого*
```text
scp -i ~/.ssh/<путь до вашего закрытого ключа> . <имя пользователя на сервере>@<ip-сервера>:/home/yc-user/foodhelper/infra/
```

- *Заходим снова на сервер, как показано ранее. И выполняем команду запуска docker-compose:*
```text
cd foodhelper/infra/ && sudo docker-compose up -d
```
- *Соберите статику:*
```
docker compose exec backend python manage.py collectstatic --no-input
```
- *Создайте файлы миграций:*
```
docker compose exec backend python manage.py makemigrations 
```

- *Примените миграции:*
```
docker compose exec backend python manage.py migrate
```

- *Создайте суперпользователя Django:*
```
docker compose exec backend python manage.py createsuperuser
```

- *Для загрузки данных из csv файлов:*
```
docker compose exec backend python manage.py import_csv
```

Выше описанная процедура может быть автоматизирована и произведено развертывание и управление процессами CI/CD с помощью workflow main.yml.
В конкретном случае запуск происходит автоматически при отправке проекта на сервер разработчика (git push).
Предварительно на github action создаются секретные ключи(DOCKER_PASSWORD, DOCKER_USERNAME, (HOST, SSH_KEY, SSH_PASSPHRASE, USER) - данные для аутентификации на виртуальной машине)

***
## Пример главной страницы работающего проекта

[Пример главной страницы с рецептами](foto1.png) - Страница с рецептами доступна для чтения.
[Пример страницы с подписками](foto1.png) - Страница с подписками на авторов рецептов.

[Проект доступен по адресу](https://foodhelper.ddns.net/) - Главная страница проекта.

***
**Над проектом работал:** [Мишков Андрей](https://github.com/MartiAndrew)