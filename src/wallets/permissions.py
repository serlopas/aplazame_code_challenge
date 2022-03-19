from rest_framework import permissions


class WalletsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_commerce and \
            request.user.wallets.exists():
            return False

        return True


class WalletsIsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class WalletsTopUpPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_customer


class WalletsChargePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_commerce
