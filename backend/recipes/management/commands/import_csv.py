import csv

from django.core.management import BaseCommand
from django.db import DatabaseError, IntegrityError

from foodhelper.settings import BASE_DIR

from recipes.models import Ingredient, Tag


class ImportDataError(Exception):
    """Исключение, возникающее при ошибке импорта данных"""
    pass


TABLES = {
    Ingredient: 'ingredients.csv',
    Tag: 'tags.csv'
}

CSV_FILE_PATH = BASE_DIR / 'data'


class Command(BaseCommand):
    """Команда для импортирования тэгов и ингридиентов
    в базу данных из csv файла."""
    help = 'Импортирует данные из CSV-файлов в базу данных'

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            try:
                with open(
                        CSV_FILE_PATH / csv_f, encoding='utf-8'
                ) as csv_file:
                    for record in csv.DictReader(csv_file):
                        model.objects.get_or_create(**record)
            except FileNotFoundError:
                raise ImportDataError(f'Файл {csv_f} не найден')
            except csv.Error:
                raise ImportDataError(f'Ошибка при чтении файла {csv_f}')
            except IntegrityError as error:
                raise ImportDataError(f'Ошибка целостности данных: {error}')
            except DatabaseError as error:
                raise ImportDataError(f'Ошибка базы данных: {error}')
        self.stdout.write(
            self.style.SUCCESS('Успешная запись в базу данных!'))
