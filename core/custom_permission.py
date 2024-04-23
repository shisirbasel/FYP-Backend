from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsNotAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            raise PermissionDenied("Admin users are not allowed to perform this action.")
        return True
