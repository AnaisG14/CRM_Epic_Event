from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorizedToAccessClientOrContract(BasePermission):
    """ Sailors can display all clients or contracts but only delete or update theirs.
        Sailors can create client and contract.
        Supporter can only see clients or contacts assigned to them and
        they can't create/update clients or contracts."""

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


class IsAuthorizedSailorOrAssignedSupporterToManageEvents(BasePermission):
    """
    Sailors can display all events but only delete or update theirs.
    Sailors can create events.
    Supporter can only see and update events assigned to them.
    They can't create/delete events.
    """

    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PUT':
            return bool(request.user.role == 'SAILOR' or request.user.role == 'SUPPORT')
        else:
            return bool(request.user.role == 'SAILOR')

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            return bool((obj.support_contact == request.user and obj.event_status == 'IN PROGRESS') or obj.client.sales_contact == request.user)

