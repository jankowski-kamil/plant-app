from rest_framework.routers import SimpleRouter

from plant.plants.api.views import PlantViewSet, RankingViewSet, WateringViewSet

app_name = "plants"

router = SimpleRouter()
router.register("plants", PlantViewSet, basename="plants")
router.register("waterings", WateringViewSet, basename="watering")
router.register("ranking", RankingViewSet, basename="rankings")

urlpatterns = router.urls
