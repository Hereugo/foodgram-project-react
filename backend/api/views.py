from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser import views as djoser_views
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Subscription,
    Tag,
)

from .custom_permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAuthorOrReadOnly,
)
from .filters import IngredientFilter, RecipeFilter
from .pagination import PageLimitPagination
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeIngredient,
    RecipeInShortSerializer,
    RecipeSerializer,
    TagSerializer,
    UserSerializer,
    UserWithRecipesSerializer,
)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    """API для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """API для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientFilter]
    search_fields = ['^name']
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """API для работы с рецептами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    )
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create',
                           'update',
                           'partial_update'):
            return RecipeCreateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart',
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            obj = ShoppingCart.objects.create(user=user, recipe=recipe)
            obj.save()
            serializer = RecipeInShortSerializer(
                recipe,
                context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            obj = ShoppingCart.objects.filter(user=user, recipe=recipe)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='favorite',
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            obj = Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeInShortSerializer(
                recipe,
                context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            obj = Favorite.objects.filter(user=user, recipe=recipe)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)


    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        recipes = ShoppingCart.objects.filter(user=request.user)

        shopping_cart = {}
        for recipe in recipes:
            ingredients = RecipeIngredient.objects.filter(recipe=recipe.recipe)
            for ingredient in ingredients:
                ingredient_name = ingredient.ingredient.name
                if ingredient_name not in shopping_cart:
                    shopping_cart[ingredient_name] = {
                        'measurement_unit': ingredient.ingredient.measurement_unit,
                        'amount': int(ingredient.amount)
                    }
                else:
                    shopping_cart[ingredient_name]['amount'] += int(ingredient.amount)

        file_content = ''
        for ingredient_name in shopping_cart:
            file_content += (
                f'{ingredient_name} - '
                f'{shopping_cart[ingredient_name]["amount"]} '
                f'{shopping_cart[ingredient_name]["measurement_unit"]}\n'
            )

        file_name = 'shopping_cart'
        response = HttpResponse(file_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={file_name}.txt'
        return response


class UserViewSet(djoser_views.UserViewSet):
    """API для работы с пользователями."""

    serializer_class = UserSerializer
    pagination_class = PageLimitPagination
    lookup_field = 'pk'

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribers__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = UserWithRecipesSerializer(
            pages,
            many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            obj = Subscription.objects.create(user=user, author=author)
            obj.save()
            serializer = UserWithRecipesSerializer(
                author,
                context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            obj = Subscription.objects.filter(user=user, author=author)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
