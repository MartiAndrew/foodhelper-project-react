from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс разрешения для админа и просто чтения."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Класс разрешения для автора или чтения"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )
