from rest_framework.permissions import BasePermission
from restaurants.models import Restaurant


class IsOwnerOrReadOnly(BasePermission):
    message = "you must have permission to make any changes on this object"

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        else:
            if request.user == obj.user.user:
                return True
            else:
                return False

    def has_permission(self, request, view):
        if request.method == "POST":
            profile = request.user.profile
            if not isinstance(profile, Restaurant):
                self.message = "only a Restaurant profile can create a Menu"
                return False
            else:
                request.data["restaurant"] = request.user.profile.pk
                return True
        return super().has_permission(request, view)


class IsProfileOrReadOnly(BasePermission):
    message = "you must have permission to make any changes on this object"

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        else:
            if request.user == obj.user:
                return True
            else:
                return False
