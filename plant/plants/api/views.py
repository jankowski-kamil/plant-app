from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from plant.channel_config.consumers import send_message_via_websocket
from plant.notifications.models import Notification

from plant.permissions.owner_permissions import IsOwnerOrReadOnly
from plant.permissions.staff_permisions import IsStaffAndCanWatering
from plant.plants.api.serializers import PlantSerializer, PlantWateringSerializer
from plant.plants.models import Plant, Watering


class PlantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PlantSerializer
    queryset = Plant.objects.prefetch_related("waterings", "owner", "staff")

    def get_queryset(self):
        is_watered = self.request.query_params.get("is_watered")
        qs = super().get_queryset().with_is_watered_information()

        if is_watered:
            is_watered = is_watered.lower() == "true"
            return qs.filter(is_watered=is_watered)

        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WateringViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStaffAndCanWatering]
    serializer_class = PlantWateringSerializer
    queryset = Watering.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        plant = serializer.validated_data["plant"]
        Notification.objects.create(
            recipient=plant.owner,
            text=f"Plant {plant.name} is now watering",
            created_by=self.request.user,
        )
        message = {
            "messages": f"Plant {plant.name} is now watering",
            "type": "unread_status"
        }
        send_message_via_websocket(self.request.user, message)




