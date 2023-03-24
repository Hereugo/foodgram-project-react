import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для загрузки ингредиентов"""

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Загрузка ингредиентов'))
        with open('data/ingredients.json', encoding='utf-8') as file:
            ingredients = json.loads(file.read())
            for ingredient in ingredients:
                Ingredient.objects.get_or_create(**ingredient)

        self.stdout.write(self.style.SUCCESS('Ингредиенты загружены'))
