from rest_framework.permissions import BasePermission


class IsAdminOrOwnUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
    
        if request.method == 'GET':
            return True
        elif request.method == 'DELETE':
            return request.user.is_superuser
        else:
            if request.user.is_superuser or request.user==obj:
                return True
            return False