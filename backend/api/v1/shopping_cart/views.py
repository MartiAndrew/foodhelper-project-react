from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe, RecipeIngredient, ShoppingCart

from users.models import User

from ...mixins import FavoriteShoppingMixin
from .pdf_generate import pdf_generate
from .serializers import ShoppingCartSerializer


class ShoppingCartView(APIView, FavoriteShoppingMixin):
    """Класс представления для корзины покупок"""

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated], )
    def shopping_cart(self, request, **kwargs):
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))

        if request.method == 'POST':
            return self.perform_action(
                user, recipe, ShoppingCartSerializer, ShoppingCart, request)
        elif request.method == 'DELETE':
            return self.delete_action(user, recipe, ShoppingCart)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated], )
    def download_shopping_cart(self, request):
        """Метод получения и выгрузки в PDF-file списка покупок."""
        if not request.user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .prefetch_related('ingredient')
            .values(
                'ingredient__name',
                'ingredient__measurement_unit',
            )
            .annotate(sum_amount=Sum('amount')).order_by()
        )
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment;'
        text_cart = ''
        for value in ingredients:
            text_cart += ' '.join([
                value['ingredient__name'],
                '-',
                str(value['sum_amount']),
                value['ingredient__measurement_unit'],
                '<br/>'
            ])
        return pdf_generate(text_cart, response)