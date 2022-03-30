from rest_framework.permissions import BasePermission

class IsMe(BasePermission):
    def has_permission(self, request, view):
        return view.kwargs.get('pk') == request.user.id