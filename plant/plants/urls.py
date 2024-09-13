from rest_framework.routers import SimpleRouter

from plant.plants.api.views import (
    PlantFamilyViewSet,
    PlantViewSet,
    RankingViewSet,
    WateringViewSet,
)

app_name = "plants"

router = SimpleRouter()
router.register("plants", PlantViewSet, basename="plants")
router.register("waterings", WateringViewSet, basename="watering")
router.register("ranking", RankingViewSet, basename="rankings")
router.register("families", PlantFamilyViewSet, basename="families")

urlpatterns = router.urls
