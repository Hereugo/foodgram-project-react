from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    """Права доступа только для чтения."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthenticated(permissions.BasePermission):
    """Права доступа только для авторизованных."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAuthor(permissions.BasePermission):
    """Права доступа только для создателей."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Права доступа для чтения всем, а для записи только для авторизованных."""

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Права доступа для редактирования и удаления только для создателей."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
