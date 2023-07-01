from djoser.serializers import UserCreateSerializer

from users.models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для модели CustomUser"""

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')
