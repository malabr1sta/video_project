from rest_framework import permissions


class IsOwnerOrPublished(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.is_published:
            return True
        return obj.owner == request.user


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
