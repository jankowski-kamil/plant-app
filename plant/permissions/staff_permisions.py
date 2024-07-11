from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsStaffAndCanWatering(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return False

        if request.user in obj.staff:
            return False

