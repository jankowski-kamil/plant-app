from rest_framework.permissions import BasePermission
from rest_framework import permissions

from plant.plants.models import Plant


class IsStaffAndCanWatering(BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return Plant.objects.filter(
            id=request.data["plant"], staff=request.user
        ).exists()
