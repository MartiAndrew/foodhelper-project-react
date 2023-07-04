from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser, Subscribe

from .serializers import (CustomUserCreateSerializer,
                          SubscribeSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],

    )
    def subscribe(self, request, **kwargs):
        user = get_object_or_404(CustomUser, id=kwargs.get('id'))
        subscribe = Subscribe.objects.filter(user=request.user, author=user)
        if request.method == 'POST':
            if user == request.user:
                msg = {'error': 'Нельзя подписаться на самого себя.'}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            obj, created = Subscribe.objects.get_or_create(
                user=request.user,
                author=user
            )
            if not created:
                msg = {'error': 'Вы уже подписаны на этого пользователя.'}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            serializer = SubscribeSerializer(obj, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not subscribe.exists():
            msg = {'error': 'Вы не подписаны на этого пользователя.'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],

    )
    def subscriptions(self, request):
        subscribe = Subscribe.objects.filter(user=request.user)
        pages = self.paginate_queryset(subscribe)
        serializer = SubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
