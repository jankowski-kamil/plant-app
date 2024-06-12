from datetime import timedelta

from django.db.models import BooleanField, Case, DateTimeField, ExpressionWrapper, F, Value, When
from django.db.models.functions import Now

from .models import models


class PlantQuerySet(models.QuerySet):

    def with_is_watered_information(self):
        queryset = self.annotate(
            next_watering=ExpressionWrapper(
                F("last_watering") + timedelta(days=1) * F('interval_watering'),
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
        return queryset

class PlantManager(models.Manager):

    def get_queryset(self):
        return PlantQuerySet(self.model, using=self._db)

    def with_is_watered_information(self, params):
        return self.get_queryset().with_is_watered_information().filter(is_watered=params)

    def all_plants(self):
        return self.get_queryset().with_is_watered_information()