from rest_framework import serializers
from plant.plants.models import Plant

class PlantSerializer(serializers.ModelSerializer):

    is_watered = serializers.BooleanField()

    class Meta:
        model = Plant
        fields = ["name", "species", 'interval_watering', 'last_watering', 'is_watered']
