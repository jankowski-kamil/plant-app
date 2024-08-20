from rest_framework import serializers

from plant.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["recipient", "text", "created_by",]