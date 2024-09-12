from celery import shared_task

from plant.plants.models import PlantFamily
from plant.plants.requests import fetch_plant_families


@shared_task
def get_plant_families():
    families = fetch_plant_families()
    families_list = [PlantFamily(name=val) for val in families]
    PlantFamily.objects.bulk_create(families_list)
