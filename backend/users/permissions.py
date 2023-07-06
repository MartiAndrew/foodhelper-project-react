from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс разрешения для администратора,
    либо других пользователей с методом запроса GET"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Класс разрешения для автора ресурса,
    либо других аутентифицированных пользователей"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author)
