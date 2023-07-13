from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag, User


class IngredientSearchFilter(SearchFilter):
    """Класс для поиска ингридиентов по имени"""
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    """Класс"""
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())

    is_favorited = filters.NumberFilter(method='_is_favorited')
    is_in_shopping_cart = filters.NumberFilter(method='_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']

    def _is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def _is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
