from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser, Subscribe

from .serializers import (CustomUserCreateSerializer,
                          SubscribeSerializer)


class CustomUserViewSet(UserViewSet):
    """Класс представления для пользователя и его подписок."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated], )
    def subscribe(self, request, **kwargs):
        user = get_object_or_404(CustomUser, user=request.user)
        author = get_object_or_404(CustomUser, id=self.kwargs.get('id'))
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author, data=request.data, context={'request': request}, )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(Subscribe, user=user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated], )
    def subscriptions(self, request):
        subscribe = Subscribe.objects.filter(user=request.user)
        pages = self.paginate_queryset(subscribe)
        serializer = SubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
