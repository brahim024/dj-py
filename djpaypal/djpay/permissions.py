from rest_framework import permissions


class PaypalTokenValidToken(permissions.BasePermission):
    message = "Check paypal has a valid token"

    def has_object_permission(self, request, view, obj):
        print(obj)
        print(view)
        return False
