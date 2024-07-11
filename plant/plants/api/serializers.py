from rest_framework import serializers

from plant.plants.models import Plant, Watering
from plant.users.models import User


class PlantWateringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watering
        fields = ["id", "plant", "litres", "watering_date"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id" ,"email"]

class PlantSerializer(serializers.ModelSerializer):
    is_watered = serializers.BooleanField(read_only=True)
    waterings = PlantWateringSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    staff =  UserSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = [
            "id",
            "name",
            "species",
            "interval_watering",
            "last_watering",
            "is_watered",
            "waterings",
            "owner",
            "staff"
        ]

    def to_representation(self, data):
        data = super().to_representation(data)
        if len(data.get("waterings")) > 5:
            data["waterings"] = data.get("waterings")[-5]
        return data
