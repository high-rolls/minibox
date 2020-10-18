from rest_framework import permissions


class IsAdminOrCompanyAdmin(permissions.BasePermission):
    # Custom permission to allow only company administrators
    # or system administrators
    def has_permission(self, request, view):
        return request.user.is_staff or \
            request.user.groups.filter(name='Company Administrator').exists()
