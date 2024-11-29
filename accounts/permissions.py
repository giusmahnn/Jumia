from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.is_admin_user and request.is_seller_user
        


class Customer(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.is_buyer_user
        