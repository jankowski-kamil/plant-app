from django.utils import timezone
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from plant.plants.models import Plant, Watering


class PlantFactory(DjangoModelFactory):
    name = Faker("word")
    species = Faker("word")
    interval_watering = 3
    last_watering = timezone.now()

    class Meta:
        model = Plant

class WateringFactory(DjangoModelFactory):
    litres = Faker("random_int")
    watering_date  = timezone.now()
    plant = SubFactory(PlantFactory)

    class Meta:
        model = Watering

