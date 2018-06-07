from rest_framework import permissions
'''
Custom permission class to verify if user is owner of the object
'''
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, object):

        if request.method in permissions.SAFE_METHODS:
            return True

        return object.owner == request.user