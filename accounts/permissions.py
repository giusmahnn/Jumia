from rest_framework.permissions import Permission, SAFE_METHODS


class IsAdmin(Permission):
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.is_admin_user and request.is_seller_user