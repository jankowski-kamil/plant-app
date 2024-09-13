import environ
import requests
from django.conf import settings

from plant.plants.exceptions import BadRequestException


def fetch_plant_families() -> list[str]:
    env = environ.Env()
    response = requests.get(
        f"https://trefle.io/api/v1/families?token={settings.API_PLANT_TOKEN})",
        timeout=15,
    )

    if response.status_code != 200:
        raise BadRequestException(response.messages)

    plant_families = response.json()["data"]

    names = [item["name"] for item in plant_families]

    return names
