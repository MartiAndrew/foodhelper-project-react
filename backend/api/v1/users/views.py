from djoser.views import UserViewSet

from users.models import CustomUser
from .serializers import CustomUserCreateSerializer


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer
