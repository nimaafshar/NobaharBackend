from rest_framework.permissions import BasePermission


class UserGroupPermissions(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return not request.user.has_group
        elif view.action == 'my_group':
            return request.user.has_group
        else:
            return True


class UserJoinRequestPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'group_requests':
            return request.user.is_admin
        if view.action == 'create':
            return not request.user.has_group
        else:
            return True
