from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Уникальный никнэйм',
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='Почта')
    first_name = models.CharField(
        max_length=150, verbose_name='Имя'
    )
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """
    Класс описывающий модель подписки пользователя
    на автора рецепта
    """
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователя',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        related_name='following',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name="Дата создания подписки",
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_subscribe'),
        )

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
