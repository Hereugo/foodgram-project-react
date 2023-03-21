from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers

from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite,
    ShoppingCart,
    Follow,
    RecipeIngredient
)

User = get_user_model()


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    """Сериализация создания пользователя"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserSerializer(djoser_serializers.UserSerializer):
    """Сериализация пользователей"""
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'following'
        )
    
    def get_following(self, obj):
        request = self.context.get('request')
        user = request.user

        if not user or user.is_anonymous:
            return False

        queryset = Follow.objects.filter(user=user, author=obj)
        return queryset.exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализация тегов"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализация ингредиентов"""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализация ингредиентов рецепта"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализация рецептов"""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user

        if not user or user.is_anonymous:
            return False
        
        queryset = Favorite.objects.filter(user=user, recipe=obj)
        return queryset.exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user

        if not user or user.is_anonymous:
            return False
        
        queryset = ShoppingCart.objects.filter(user=user, recipe=obj)
        return queryset.exists()
