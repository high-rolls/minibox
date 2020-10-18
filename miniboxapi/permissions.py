from rest_framework import permissions


class IsCompanyAdministrator(permissions.BasePermission):
    # Custom permission to allow only company administrators
    # or system administrators
    def has_permission(self, request, view):
        request.user.groups.filter(name='Company Administrator').exists()
