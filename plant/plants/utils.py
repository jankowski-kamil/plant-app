from django.db.models import Avg, F, Sum
from django.shortcuts import get_object_or_404

from plant.plants.api.serializers import PlantStatsSerializer
from plant.plants.models import Plant
from plant.plants.types import ParamsDateRange


def create_stats(params: ParamsDateRange, pk):
    plant = get_object_or_404(Plant, pk=pk)
    the_most_active_users = (
        plant.waterings.values("user")
        .order_by("user")
        .annotate(total_litres=Sum("litres"))[:3]
    )
    average_watering_per_month = plant.waterings.values(
        month=F("watering_date__month"),
    ).annotate(average_litres=Avg("litres"))

    waterings_count = plant.waterings.filter(
        watering_date__range=(
            params["start_date"],
            params["end_date"],
        ),
    ).count()

    response_serializer = PlantStatsSerializer(
        {
            "active_user": the_most_active_users,
            "average_watering_per_month": average_watering_per_month,
            "waterings_count": waterings_count,
        },
    )

    return response_serializer
