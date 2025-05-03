from rest_framework import permissions

class IsProfessionalUser(permissions.BasePermission):
    """
    Allows access only to users with the 'professional' role.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'professional'
