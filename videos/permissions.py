from rest_framework import permissions


class IsOwnerOrPublished(permissions.BasePermission):
    """
    Custom permission to allow access if the user is the owner, the object
    is published, or the user is staff.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check object-level permissions.

        Args:
            request: DRF request object.
            view: DRF view object.
            obj: The object being accessed.

        Returns:
            bool: True if the user is staff, the object is published, or
            the user is the owner.
        """
        if request.user.is_staff:
            return True
        if obj.is_published:
            return True
        return obj.owner == request.user


class IsStaff(permissions.BasePermission):
    """
    Custom permission to allow access only to authenticated staff users.
    """
    def has_permission(self, request, view):
        """
        Check general permission.

        Args:
            request: DRF request object.
            view: DRF view object.

        Returns:
            bool: True if the user is authenticated and is staff.
        """
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
