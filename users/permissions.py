from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.groups.filter(name='moderator').exists() or request.user == obj.author
