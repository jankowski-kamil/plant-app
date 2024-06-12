from rest_framework import  viewsets
from rest_framework.permissions import AllowAny

from plant.plants.models import Plant
from .serializers import PlantSerializer

class PlantsList(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def get_queryset(self):
        params = self.request.query_params.get('is_watered')
        queryset = Plant.objects.all()
        print(queryset)
        if params is not None:
            return queryset.filter(is_watered=params)
        return queryset

