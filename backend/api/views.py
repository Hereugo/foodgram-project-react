from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from djoser import views as djoser_views

from .serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    UserSerializer,
)
from .custom_permissions import (
    IsAuthorOrReadOnly,
    IsAuthenticatedOrReadOnly
)
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    """API для работы с тегами."""
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """API для работы с ингредиентами."""
    
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    """API для работы с рецептами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    )
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(djoser_views.UserViewSet):
    """API для работы с пользователями."""

    serializer_class = UserSerializer
