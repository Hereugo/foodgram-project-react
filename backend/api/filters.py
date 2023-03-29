from django.contrib.auth import get_user_model
from django_filters.rest_framework import (
    BooleanFilter,
    FilterSet,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    author = ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='author__username',
        label='Автор'
    )
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
        label='Теги'
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart',
        label='В корзине'
    )
    is_favorited = BooleanFilter(
        field_name='is_favorited',
        method='filter_is_favorited',
        label='В избранном'
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_in_shopping_cart',
            'is_favorited',
        )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user or user.is_anonymous:
            return queryset

        if value:
            return queryset.filter(shopping_cart__user=user)

        return queryset.exclude(shopping_cart__user=user)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not user or user.is_anonymous:
            return queryset

        if value:
            return queryset.filter(favorite__user=user)

        return queryset.exclude(favorite__user=user)
