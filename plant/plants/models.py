from django.db import models

from plant.plants.managers import PlantQuerySet


class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    interval_watering = models.IntegerField()
    last_watering = models.DateTimeField()
    objects = PlantQuerySet.as_manager()

    def __str__(self):
        return self.name
