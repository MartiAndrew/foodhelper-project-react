from django.contrib import admin

from .models import (Tag, AmountRecipe, Favorites,
                     Ingredient, Recipe, ShoppingCart)

EMPTY_MESSAGE = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    """Представляет модель Tag в интерфейсе администратора."""
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    empty_value_display = EMPTY_MESSAGE


class AmountRecipeInline(admin.TabularInline):
    """Представляет модель AmountRecipe в интерфейсе администратора."""
    model = AmountRecipe


class IngredientAdmin(admin.ModelAdmin):
    """Представляет модель Ingredient в интерфейсе администратора."""
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = (AmountRecipeInline,)
    empty_value_display = EMPTY_MESSAGE


class RecipeAdmin(admin.ModelAdmin):
    "Представляет модель Recipe в интерфейсе пользователя."
    list_display = ('id', 'name', 'author', 'cooking_time',
                    'favorite_count', 'list_ingredients')
    search_fields = ('author', 'name', 'tags')
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags',)
    inlines = (AmountRecipeInline,)
    empty_value_display = EMPTY_MESSAGE

    def favorite_count(self, obj):
        if obj.favorite_recipe.exists():
            return obj.favorite_recipe.count()
        return 0

    favorite_count.short_description = 'Избранное'

    def list_ingredients(self, obj):
        if obj.ingredients.exists():
            return ', '.join(
                [str(ingredient) for ingredient in obj.ingredients.all()]
            )
        return 0

    list_ingredients.short_description = 'Ингредиенты'


class FavoritesAdmin(admin.ModelAdmin):
    """Представляет модель Favorites в интерфейсе администратора."""
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_MESSAGE


class ShoppingCartAdmin(admin.ModelAdmin):
    """Представляет модель ShoppingCart в интерфейсе администратора."""
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_MESSAGE


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
