from django.shortcuts import render
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from plant.notifications.api.serializers import NotificationSerializer
from plant.notifications.models import Notification


# Create your views here.

class NotificationListView(ListModelMixin,GenericViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationUserListView(ListModelMixin,GenericViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user)