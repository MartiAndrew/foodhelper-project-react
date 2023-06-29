from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "password")
    list_filter = ("username", "email")
    empty_value_display = '-пусто-'



admin.site.register(CustomUser, UserAdmin)

