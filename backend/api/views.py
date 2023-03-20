from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer
from recipes.models import Recipe, Tag, Ingredient


class TagViewSet(ModelViewSet):
    """API для работы с тегами."""
    pass


class RecipeViewSet(ModelViewSet):
    """API для работы с рецептами."""
    pass


class IngredientViewSet(ModelViewSet):
    """API для работы с ингредиентами."""
    pass


class UserViewSet(ModelViewSet):
    """API для работы с пользователями."""
    pass
