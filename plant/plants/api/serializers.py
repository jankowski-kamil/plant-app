from rest_framework import serializers

from plant.plants.models import Plant, Watering


class PlantWateringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watering
        fields = ['plant', 'litres', 'watering_date']

class PlantSerializer(serializers.ModelSerializer):
    is_watered = serializers.BooleanField()
    watering = PlantWateringSerializer(many=True)

    class Meta:
        model = Plant
        fields = ["name", "species", "interval_watering", "last_watering", "is_watered", 'watering']

    def to_representation(self, data):
        data = super().to_representation(data)
        if len(data.get('watering')) > 5:
            data['watering'] = data.get('watering')[-5]
        return data





