
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import PlantSerializer
from ..models import Plant


class PlantViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PlantSerializer

    def get_queryset(self):
        params = self.request.query_params.get("is_watered")
        if params is not None:
            return Plant.object.with_is_watered_information(params)
        return Plant.object.all_plants()
