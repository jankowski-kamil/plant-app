from django.db import models

from plant.plants.managers import PlantManager


class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    interval_watering = models.IntegerField()
    last_watering = models.DateTimeField()
    object = PlantManager()

    def __str__(self):
        return self.name

