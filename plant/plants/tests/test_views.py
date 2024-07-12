import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status


from plant.plants.tests.factories import PlantFactory, WateringFactory
from plant.users.tests.factories import UserFactory


class TestPlantViewSet:

    @pytest.mark.django_db()
    def test_list_plants(self, api_client, user):
        plants = PlantFactory.create_batch(size=5)
        api_client.force_authenticate(user=user)
        url = reverse("plants:plants-list")
        response = api_client.get(url)
        assert response.data[0]["name"] == plants[0].name
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_get_plant(self, api_client, user):
        api_client.force_authenticate(user=user)
        plants = PlantFactory.create_batch(size=5)
        url = reverse("plants:plants-detail", kwargs={"pk": plants[0].id})
        response = api_client.get(url)
        assert response.data["name"] == plants[0].name
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_delete_plant(self, api_client, user):
        api_client.force_authenticate(user=user)
        PlantFactory.create_batch(size=5)
        url = reverse("plants:plants-list")
        payload = {
            "name": "New plant",
            "species": "New description",
            "interval_watering": 2,
            "last_watering": timezone.now(),
        }
        plant = api_client.post(url, payload)
        url = reverse("plants:plants-detail", kwargs={"pk": plant.data["id"]})
        url_plants_list = reverse("plants:plants-list")
        response = api_client.delete(url)
        plants_list = api_client.get(url_plants_list)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(plants_list.data) == 5

    @pytest.mark.django_db()
    def test_add_plant(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("plants:plants-list")
        payload = {
            "name": "New plant",
            "species": "New description",
            "interval_watering": 2,
            "last_watering": timezone.now(),
        }
        response = api_client.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == payload["name"]

    @pytest.mark.django_db()
    def test_watering_list(self, api_client, user):
        api_client.force_authenticate(user=user)
        waterings = WateringFactory.create_batch(size=5)
        url = reverse("plants:watering-list")
        response = api_client.get(url)
        assert response.data[0]["litres"] == waterings[0].litres
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_watering_detail(self, api_client, user):
        api_client.force_authenticate(user=user)
        waterings = WateringFactory.create_batch(size=5)
        url = reverse("plants:watering-detail", kwargs={"pk": waterings[0].id})
        response = api_client.get(url)
        assert response.data["litres"] == waterings[0].litres
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_permission_delete_plant(self, api_client, user):
        new_user = UserFactory()
        api_client.force_authenticate(user=user)
        url = reverse("plants:plants-list")
        payload = {
            "name": "New plant",
            "species": "New description",
            "interval_watering": 2,
            "last_watering": timezone.now(),
        }
        plant = api_client.post(url, payload)
        api_client.force_authenticate(user=new_user)
        url = reverse("plants:plants-detail", kwargs={"pk": plant.data["id"]})
        url_plants_list = reverse("plants:plants-list")
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


