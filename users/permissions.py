from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name='moderator').exists() or request.user.is_superuser


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.author or request.user.is_superuser
