from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .v1.users.views import (CustomUserViewSet)

app_name = "api"

router_v1 = DefaultRouter()

router_v1.register('users', CustomUserViewSet, basename='users')



urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
