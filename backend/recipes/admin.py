from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 1


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 1


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug', 'usage_count')
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    def usage_count(self, obj):
        return obj.recipes.count()

    usage_count.short_description = 'Количество использований'
    usage_count.admin_order_field = 'usage_count'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit', 'usage_count')
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    def usage_count(self, obj):
        return obj.recipes.count()

    usage_count.short_description = 'Количество использований'
    usage_count.admin_order_field = 'usage_count'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'text',
        'cooking_time',
        'author',
        'get_ingredients_count',
        'get_shopping_cart_count',
        'get_favorites_count',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    inlines = (
        RecipeTagInline,
        RecipeIngredientInline,
        ShoppingCartInline,
        FavoriteInline,
    )

    def get_ingredients_count(self, obj):
        return obj.ingredients.count()

    get_ingredients_count.short_description = 'Количество ингредиентов'
    get_ingredients_count.admin_order_field = 'get_ingredients_count'

    def get_shopping_cart_count(self, obj):
        return obj.shopping_cart.count()

    get_shopping_cart_count.short_description = 'Количество в корзине'
    get_shopping_cart_count.admin_order_field = 'get_shopping_cart_count'

    def get_favorites_count(self, obj):
        return obj.favorite.count()

    get_favorites_count.short_description = 'Количество в избранном'
    get_favorites_count.admin_order_field = 'get_favorites_count'
