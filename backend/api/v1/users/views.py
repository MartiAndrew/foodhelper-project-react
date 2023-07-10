from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from django.db.models.expressions import Exists, OuterRef, Value
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser, Subscribe

from .serializers import (CustomUserCreateSerializer,
                          SubscribeSerializer, CustomUserSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Класс представления для пользователя и его подписок."""
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """В этом методе аннотируется каждый объект пользователя (User)
        значением is_subscribed, которое указывает, подписан ли текущий
        аутентифицированный пользователь на данного пользователя.
        Подзапрос (Exists) проверяет, существуют ли связи follower между
        текущим пользователем (self.request.user) и объектом пользователя,
        ссылающегося на текущего пользователя (author=OuterRef('id')"""
        queryset = CustomUser.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_subscribed=Exists(
                    self.request.user.follower.filter(author=OuterRef('id'))
                )
            ).prefetch_related('follower', 'following')
        else:
            queryset = queryset.annotate(is_subscribed=Value(False))
        return queryset

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """Метод получения подписки пользователя."""
        subscribe = Subscribe.objects.filter(user=request.user)
        pages = self.paginate_queryset(subscribe)
        serializer = SubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class SubscribeCreateDel(
        generics.RetrieveDestroyAPIView,
        generics.ListCreateAPIView):
    """Класс представления для подписки и отписки от пользователя."""

    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.request.user.follower.select_related(
            'following'
        ).prefetch_related(
            'following__recipe'
        ).annotate(
            recipes_count=Count('following__recipe'),
            is_subscribed=Value(True), )

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(self.request, user)
        return user

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        instance = get_object_or_404(User, id=user_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subs = serializer.save(author=instance, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        self.request.user.follower.filter(author=instance).delete()

