from rest_framework import permissions


class IsAdminOrOwnUser(permissions.BasePermission):
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
    
class IsOwnUser(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.user.is_superuser:
            return True
        return request.user==obj.user
        