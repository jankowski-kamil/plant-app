from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg, F, Count
from datetime import datetime, timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework.viewsets import GenericViewSet

from plant.channel_config.consumers import send_message_via_websocket
from plant.plants.filters import RankingFilters
from plant.notifications.models import Notification
from rest_framework.response import Response
from plant.permissions.owner_permissions import IsOwnerOrReadOnly
from plant.permissions.staff_permisions import IsStaffAndCanWatering
from plant.plants.api.serializers import (
    PlantSerializer,
    PlantWateringSerializer,
    TheMostActiveUsersSerializer,
    AverageWateringPerMonthSerializer,
    RankingSerializer,
)
from plant.plants.models import Plant, Watering


class PlantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PlantSerializer
    queryset = Plant.objects.prefetch_related("waterings", "owner", "staff")

    def get_queryset(self):
        is_watered = self.request.query_params.get("is_watered")
        qs = super().get_queryset().with_is_watered_information()

        if is_watered:
            is_watered = is_watered.lower() == "true"
            return qs.filter(is_watered=is_watered)

        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["GET"])
    def plant_stats(self, request, pk=None):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        plant = get_object_or_404(Plant, pk=pk)
        the_most_active_users = (
            plant.waterings.values("user")
            .order_by("user")
            .annotate(total_litres=Sum("litres"))[:3]
        )
        average_watering_per_month = plant.waterings.values(
            month=F("watering_date__month")
        ).annotate(average_litres=Avg("litres"))

        print(start_date, end_date)

        if start_date and end_date:
            waterings_count = plant.waterings.filter(
                watering_date__range=(start_date, end_date)
            ).count()
        else:
            waterings_count = plant.waterings.filter(
                watering_date__lte=datetime.now() - timedelta(days=30)
            ).count()

        average_serializer = AverageWateringPerMonthSerializer(
            average_watering_per_month, many=True
        )
        active_user_serializer = TheMostActiveUsersSerializer(
            the_most_active_users, many=True
        )

        return Response(
            {
                "active_user": active_user_serializer.data,
                "average_watering_per_month": average_serializer.data,
                "waterings_count": waterings_count,
            },
            status=status.HTTP_200_OK,
        )


class WateringViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStaffAndCanWatering]
    serializer_class = PlantWateringSerializer
    queryset = Watering.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        plant = serializer.validated_data["plant"]
        Notification.objects.create(
            recipient=plant.owner,
            text=f"Plant {plant.name} is now watering",
            created_by=self.request.user,
        )
        message = {
            "messages": f"Plant {plant.name} is now watering",
            "type": "unread_watering_notifications",
        }
        send_message_via_websocket(self.request.user, message)


class RankingViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RankingSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("user",)
    ordering_fields = ["total_litres", "count_waterings"]
    filterset_class = RankingFilters

    def get_queryset(self):
        return (
            Watering.objects.values("user")
            .annotate(total_litres=Sum("litres"))
            .annotate(count_waterings=Count("id"))
            .annotate()
        )


