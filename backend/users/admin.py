from django.contrib import admin

from users.models import Subscribe, User

EMPTY_MESSAGE = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    """
    Представление модели пользователя в интерфейсе администратора
    """
    list_display = ("id", "username", "email",
                    "first_name", "last_name", "password")
    list_filter = ("username", "email")
    empty_value_display = EMPTY_MESSAGE


class SubscribeAdmin(admin.ModelAdmin):
    """Представляет модель Subscribe в интерфейсе администратора."""
    list_display = ('id', 'user', 'author')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_MESSAGE


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
