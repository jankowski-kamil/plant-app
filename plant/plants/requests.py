import environ
import requests


def fetch_plant_families():
    env = environ.Env()
    response = requests.get(
        f"https://trefle.io/api/v1/families?token={env("API_PLANT")}", timeout=15
    )

    if response.status_code != 200:
        raise Exception(response.json())

    plant_families = response.json()["data"]

    names = [item["name"] for item in plant_families]

    return names
