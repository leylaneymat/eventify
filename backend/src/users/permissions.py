from rest_framework.permissions import BasePermission

from users.models import User


class AllowCreate(BasePermission):
    
    def has_permission(self, request, view):
        if request.method == "POST":
            return True


class IsAdminOrIsOwner(BasePermission):
        
    def has_permission(self, request, view):
        user_pk = view.kwargs.get("user_pk")
        return bool(
            request.user.is_staff or
            request.user == User.objects.filter(pk=user_pk).first()
        )
