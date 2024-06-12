from rest_framework.routers import SimpleRouter

from plant.plants.api.views import PlantViewSet

app_name = "plants"

router = SimpleRouter()
router.register("", PlantViewSet, basename="plants")

urlpatterns = router.urls
