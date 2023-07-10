from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .v1.favorites.views import FavoriteCreateDel
from .v1.shopping_cart.views import ShoppingCartCreateDel
from .v1.users.views import CustomUserViewSet
from .v1.tags.views import TagViewSet
from .v1.ingredient.views import IngredientViewSet
from .v1.recipe.views import RecipeViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/',
          FavoriteCreateDel.as_view(),
          name='favorite_recipe'),
    path('recipes/<int:recipe_id>/shopping_cart/',
          ShoppingCartCreateDel.as_view(),
          name='shopping_cart'),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
