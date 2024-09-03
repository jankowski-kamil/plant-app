from django.urls import path
from rest_framework.routers import SimpleRouter

from plant.plants.api.views import PlantViewSet, WateringViewSet, RankingViewSet

app_name = "plants"

router = SimpleRouter()
router.register("plants", PlantViewSet, basename="plants")
router.register("waterings", WateringViewSet, basename="watering")
router.register("ranking", RankingViewSet, basename="rankings")

urlpatterns = router.urls
