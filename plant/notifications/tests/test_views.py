import pytest
from django.urls import reverse
from rest_framework import status

from plant.notifications.models import Notification

from .factories import NotificationFactory


class TestNotificationsViewSet:
    @pytest.mark.django_db()
    def test_list_notifications(self, api_client, user):
        notifications = NotificationFactory.create_batch(size=5)
        api_client.force_authenticate(user=user)
        url = reverse("notifications:notifications-list")
        response = api_client.get(url)
        assert len(response.data) == len(notifications)
        assert response.status_code == status.HTTP_200_OK

    def test_user_unauthorized_notifications(self, api_client, user):
        NotificationFactory.create_batch(size=5)
        url = reverse("notifications:user-notifications-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_without_notifications(self, api_client, user):
        NotificationFactory.create_batch(size=5)
        api_client.force_authenticate(user=user)
        url = reverse("notifications:user-notifications-list")
        response = api_client.get(url)
        assert len(response.data) == 0

    def test_user_notifications(self, api_client, user):
        Notification.objects.create(
            recipient=user,
            text="Plant TEST is now watering",
            created_by=user,
        )
        api_client.force_authenticate(user=user)
        url = reverse("notifications:user-notifications-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
