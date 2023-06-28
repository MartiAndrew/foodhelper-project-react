from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Уникальный никнэйм',
        error_messages={
            'unique': "Пользователь с таким никнеймом уже существует.",
        }
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='Почта')
    first_name = models.CharField(
        max_length=150, verbose_name='Имя'
    )
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username





