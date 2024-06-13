from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from plant.plants.api.serializers import PlantSerializer, PlantWateringSerializer
from plant.plants.models import Plant, Watering


class PlantViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()

    def get_queryset(self):
        is_watered = self.request.query_params.get("is_watered")
        qs = super().get_queryset().with_is_watered_information()

        if is_watered:
            is_watered = is_watered.lower() == "true"
            return qs.filter(is_watered=is_watered)

        return qs


class WateringViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PlantWateringSerializer
    queryset = Watering.objects.all()
