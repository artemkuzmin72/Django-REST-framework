from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Проверяет, состоит ли пользователь в группе 'Модераторы'
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
               request.user.groups.filter(name='Модераторы').exists()
    
class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True  

        if request.user.groups.filter(name='Модераторы').exists():
            return request.method in ['PUT', 'PATCH']

        return False 
    
class IsModeratorOrOwner(permissions.BasePermission):
    """
    Модератор может редактировать и просматривать все.
    Обычный пользователь — только свои объекты.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.groups.filter(name='Модераторы').exists():
            return request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH']
        else:
            if obj.owner == user:
                return True

        return False