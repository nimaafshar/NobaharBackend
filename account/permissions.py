from rest_framework.permissions import BasePermission


class UserGroupPermissions(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return not request.user.has_group
        else:
            return True
