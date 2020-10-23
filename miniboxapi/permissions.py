from rest_framework import permissions


class IsCompanyAdministrator(permissions.BasePermission):
    # Custom permission to allow only company administrators
    # or system administrators
    # I don't think this is required at all
    # There's probably a way to set view permissions to groups directly
    def has_permission(self, request, view):
        request.user.groups.filter(name='Company Administrator').exists()
