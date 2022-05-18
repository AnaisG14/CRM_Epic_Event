from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorizedToAccessClient(BasePermission):
    """ Sailors can display all clients but only delete or update theirs.
        Sailors can create client.
        Supporter can only see clients assigned to them and can't create clients."""

    message = 'You are not authorized to access these datas.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user.role == 'SAILOR' or request.user.role == 'SUPPORT')
        else:
            return bool(request.user.role == 'SAILOR')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return bool(obj.sales_contact == request.user)


class IsSupporterAssignedClientOrNoAccess(BasePermission):
    """ Supporters can display only their assigned client.
    They can't create, update or delete client."""
    pass


class CanCRUDClients(BasePermission):
    """Managers have all permissions on CRUD for all objects."""
    pass



