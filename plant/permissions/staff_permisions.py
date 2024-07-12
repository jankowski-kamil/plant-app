from rest_framework.permissions import BasePermission
from rest_framework import permissions

from plant.plants.models import Plant


class IsStaffAndCanWatering(BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        plant = Plant.objects.get(id=request.data["plant"]).all()
        if request.user in plant.staff:
            return True
        return False
