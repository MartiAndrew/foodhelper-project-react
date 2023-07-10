from django.core.exceptions import ValidationError
import django_filters as filters

from users.models import CustomUser
from recipes.models import Ingredient, Recipe


class TagsMultipleChoiceField(
        filters.fields.MultipleChoiceField):
    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages['required'],
                code='required')
        for val in value:
            if val in self.choices and not self.valid_value(val):
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},)


class TagsFilter(filters.AllValuesMultipleFilter):
    field_class = TagsMultipleChoiceField


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class CustomRecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
    is_favorited = filters.BooleanFilter(
        method='get_favorite',
        label='Favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_shopping',
        label='Is in shopping list',
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'tags',
            'is_in_shopping_cart',
        )

    def get_favorite(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            return queryset.filter(fav_recipe__user=self.request.user)
        return queryset

    def get_shopping(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            return queryset.filter(cart_recipe__user=self.request.user)
        return queryset