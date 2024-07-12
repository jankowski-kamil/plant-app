from datetime import timedelta

from django.db.models import (
    BooleanField,
    Case,
    DateTimeField,
    ExpressionWrapper,
    F,
    Value,
    When,
)
from django.db.models.functions import Now

from .models import models


class PlantQuerySet(models.QuerySet):
    def with_is_watered_information(self):
        return self.annotate(
            next_watering=ExpressionWrapper(
                F("last_watering") + timedelta(days=1) * F("interval_watering"),
                output_field=DateTimeField(),
            ),
            current_time=Now(),
        ).annotate(
            is_watered=Case(
                When(
                    current_time__lt=F("next_watering"), then=Value(True)
                ),  # noqa: FBT003
                default=Value(False),  # noqa: FBT003
                output_field=BooleanField(),
            ),
        )
