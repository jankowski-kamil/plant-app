from django.db.models import BooleanField
from django.db.models import Case
from django.db.models import DateTimeField
from django.db.models import ExpressionWrapper
from django.db.models import F
from django.db.models import Func
from django.db.models import Value
from django.db.models import When
from django.db.models.functions import Now
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from plant.plants.models import Plant

from .serializers import PlantSerializer


class Interval(Func):
    function = "INTERVAL"
    template = "(%(expressions)s * %(function)s '1' DAY)"


class PlantsList(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Plant.objects.annotate(
        next_watering=ExpressionWrapper(
            F("last_watering") + Interval("interval_watering"),
            output_field=DateTimeField(),
        ),
        current_time=Now(),
    ).annotate(
        is_watered=Case(
            When(current_time__lt=F("next_watering"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    )
    serializer_class = PlantSerializer

    def get_queryset(self):
        params = self.request.query_params.get("is_watered")
        if params is not None:
            return self.queryset.filter(is_watered=params)
        return self.queryset
