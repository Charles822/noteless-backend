from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from lists.models import List

class IsOwnerOrAdmin(BasePermission):
    
    # Custom permission to only allow owners of an object or admins to edit it.
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True


        # If the object is a user, check if it's the same as the request user
        if isinstance(obj, User):
            return obj == request.user or request.user.is_staff

        # Write permissions are only allowed to the owner of the object or admin.
        return obj.owner == request.user or request.user.is_staff


class IsListOwnerOrAdmin(BasePermission):
    
    def has_permission(self, request, view):
        # Assuming the list ID is passed in the request data
        list_id = request.data.get('note_list')
        # current_user = request.data.get('owner')
        
        # Fetch the list object (handle this with try-except if necessary)
        list_obj = List.objects.get(id=list_id)
        print(list_id)
        print('list obj owner: ', list_obj.owner)
        print(request.user)

        # Check if the user is the owner of the list or an admin
        if list_obj.owner == request.user or request.user.is_staff:
            return True
        else:
            raise PermissionDenied(detail="You do not have permission to access this list.")



class AdminOnly(BasePermission):
    
    # Custom permission to only allow admin users to access the view.
    
    def has_permission(self, request, view):
        # Check if the user is authenticated and is a staff member (admin)
        return request.user and request.user.is_staff