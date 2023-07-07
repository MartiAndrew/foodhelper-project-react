from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..recipe.mixins import FavoriteShoppingMixin
from users.models import CustomUser
from recipes.models import Recipe, ShoppingCart, AmountRecipe
from .serializers import ShoppingCartSerializer
from .pdf_generate import pdf_generate


class ShoppingCartView(APIView, FavoriteShoppingMixin):
    """Класс представления для корзины покупок"""

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated], )
    def favorite(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))

        if request.method == 'POST':
            return self.perform_action(
                user, recipe, ShoppingCartSerializer, ShoppingCart)
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
            AmountRecipe.objects.filter(
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
                str(value['amount__sum']),
                value['ingredient__measurement_unit'],
                '<br/>'
            ])
        return pdf_generate(text_cart, response)
