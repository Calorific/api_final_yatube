from rest_framework import permissions


class BasePermissionWithMessage(permissions.BasePermission):
    message = 'У вас нет прав на это действие'


class IsOwnerOrReadOnly(BasePermissionWithMessage):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsFollowerOrReadOnly(BasePermissionWithMessage):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
