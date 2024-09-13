from django.db import models

from plant.plants.managers import PlantQuerySet
from plant.users.models import User


class PlantFamily(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    interval_watering = models.IntegerField()
    last_watering = models.DateTimeField()
    objects = PlantQuerySet.as_manager()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    staff = models.ManyToManyField(User, related_name="staff", blank=True)
    family = models.ForeignKey(
        PlantFamily,
        related_name="family",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Watering(models.Model):
    plant = models.ForeignKey(Plant, related_name="waterings", on_delete=models.CASCADE)
    litres = models.IntegerField()
    watering_date = models.DateField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="waterings_user",
    )

    def __str__(self):
        return f"{self.plant.name} {self.litres} {self.watering_date}"
