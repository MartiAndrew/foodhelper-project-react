import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файлов в базу данных'

    def load_ingredients(self):
        path = f'{settings.BASE_DIR}/data/ingredients.csv'
        with open(path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            try:
                for row in reader:
                    recipes_igredient = Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=row[1]
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Ingredient {recipes_igredient.name} создан.'
                    ))
            except Ingredient.DoesNotExist:
                self.stderr.write(self.style.ERROR('Ingredient не создан'))
            except ValueError as error:
                self.stderr.write(self.style.ERROR(f'Error: {str(error)}'))

    def handle(self, *args, **options):
        self.load_ingredients()

        self.stdout.write(self.style.SUCCESS('База данных импортирована '
                                             'полностью.'))
