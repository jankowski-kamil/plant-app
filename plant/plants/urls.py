from rest_framework.routers import SimpleRouter

from plant.plants.api.views import PlantViewSet, WateringViewSet

app_name = "plants"

router = SimpleRouter()
router.register("plants", PlantViewSet, basename="plants")
router.register("waterings", WateringViewSet, basename="watering")



urlpatterns = router.urls
