from celery import shared_task

from plant.plants.models import PlantFamily
from plant.plants.requests import fetch_plant_families


@shared_task
def get_plant_families():
    families = fetch_plant_families()
    for family_name in families:
        PlantFamily.objects.get_or_create(name=family_name)
