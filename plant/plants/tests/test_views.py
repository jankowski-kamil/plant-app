import pytest
from django.urls import reverse
from django.utils import timezone

from plant.plants.tests.factories import PlantFactory, WateringFactory


class TestPlantViewSet:
    @pytest.mark.django_db()
    def test_list_plants(self, client):
        plants = PlantFactory.create_batch(size=5)
        url = reverse("plants:plants-list")
        response = client.get(url)
        assert response.data[0]["name"] == plants[0].name
        assert response.status_code == 200

    @pytest.mark.django_db()
    def test_get_plant(self, client):
        plants = PlantFactory.create_batch(size=5)
        url = reverse("plants:plants-detail", kwargs={"pk": plants[0].id})
        response = client.get(url)
        assert response.data["name"] == plants[0].name
        assert response.status_code == 200

    @pytest.mark.django_db()
    def test_delete_plant(self, client):
        plants = PlantFactory.create_batch(size=5)
        url = reverse("plants:plants-detail", kwargs={"pk": plants[0].id})
        url_plants_list = reverse("plants:plants-list")
        response = client.delete(url)
        plants_list = client.get(url_plants_list)
        assert response.status_code == 204
        assert len(plants_list.data) == 4

    @pytest.mark.django_db()
    def test_add_plant(self, client):
        url = reverse("plants:plants-list")
        payload = dict(
            name="New plant",
            species="New description",
            interval_watering=2,
            last_watering=timezone.now(),
        )
        response = client.post(url, payload)
        assert response.status_code == 201
        assert response.data["name"] == payload["name"]

    @pytest.mark.django_db()
    def test_watering_list(self, client):
        waterings = WateringFactory.create_batch(size=5)
        url = reverse("plants:watering-list")
        response = client.get(url)
        assert response.data[0]["litres"] == waterings[0].litres
        assert response.status_code == 200

    @pytest.mark.django_db()
    def test_watering_detail(self, client):
        waterings = WateringFactory.create_batch(size=5)
        url = reverse("plants:watering-detail", kwargs={"pk": waterings[0].id})
        response = client.get(url)
        assert response.data["litres"] == waterings[0].litres
        assert response.status_code == 200
