from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Chỉ cho phép admin truy cập."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Chỉ admin mới được phép
