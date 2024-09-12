from datetime import datetime, timedelta

from rest_framework import serializers

from plant.plants.models import Plant, PlantFamily, Watering
from plant.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class PlantWateringSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Watering
        fields = ["id", "plant", "litres", "watering_date", "user"]


class PlantFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantFamily
        fields = ["id", "name"]


class PlantSerializer(serializers.ModelSerializer):
    is_watered = serializers.BooleanField(read_only=True)
    family = PlantFamilySerializer(read_only=True)
    waterings = PlantWateringSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    staff = UserSerializer(many=True, read_only=True)
    staff_ids = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.all(),
        many=True,
    )

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
            "staff",
            "staff_ids",
            "family",
        ]

    def create(self, validated_data):
        staff = validated_data.pop("staff_ids")
        instance = super().create(validated_data)
        instance.staff.set(staff)
        return instance

    def update(self, instance, validated_data):
        staff = validated_data.pop("staff_ids")
        instance = super().update(instance, validated_data)
        instance.staff.set(staff)
        return instance

    def to_representation(self, data):
        data = super().to_representation(data)
        if len(data.get("waterings")) > 5:
            data["waterings"] = data.get("waterings")[-5]
        return data


class StatsParamsSerializer(serializers.Serializer):
    start_date = serializers.DateField(default=datetime.now() - timedelta(days=30))
    end_date = serializers.DateField(default=datetime.now())


class TheMostActiveUsersSerializer(serializers.Serializer):
    user = serializers.IntegerField(read_only=True)
    total_litres = serializers.IntegerField(read_only=True)


class AverageWateringPerMonthSerializer(serializers.Serializer):
    month = serializers.IntegerField(read_only=True)
    average_litres = serializers.FloatField(read_only=True)


class RankingSerializer(serializers.Serializer):
    user = serializers.IntegerField(read_only=True)
    total_litres = serializers.IntegerField(read_only=True)
    count_waterings = serializers.IntegerField(read_only=True)


class PlantStatsSerializer(serializers.Serializer):
    active_user = TheMostActiveUsersSerializer(many=True, read_only=True)
    average_watering_per_month = AverageWateringPerMonthSerializer(
        many=True,
        read_only=True,
    )
    waterings_count = serializers.IntegerField(read_only=True)
