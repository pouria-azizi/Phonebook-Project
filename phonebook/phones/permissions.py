from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.user.is_inonymous:
            return False
        if obj.user == request.user:
            return True
        return False
