from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализация рецептов"""

    class Meta:
        fields = '__all__'
        model = Recipe


class TagSerializer(serializers.ModelSerializer):
    """Сериализация тегов"""

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализация ингредиентов"""

    class Meta:
        fields = '__all__'
        model = Ingredient
