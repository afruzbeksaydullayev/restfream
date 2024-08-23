from rest_framework import permissions

class CustomPermissions(permissions.BasePermission):
    '''def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        
        return False'''
    
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
          
            if request.method in permissions.SAFE_METHODS:
                return True

            if request.method == 'DELETE' and request.user.is_superuser:
                return True
            
            if request.method in ['PUT', 'PATCH'] and request.user.is_staff:
                return True
         
               