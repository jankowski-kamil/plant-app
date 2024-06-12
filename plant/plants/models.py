from datetime import timedelta, datetime, timezone
from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    interval_watering = models.IntegerField()
    last_watering = models.DateTimeField()

    @property
    def is_watered(self):
        next_watering_day = self.last_watering + timedelta(days=self.interval_watering)
        return datetime.now(timezone.utc) < next_watering_day

    def __str__(self):
        return self.name
