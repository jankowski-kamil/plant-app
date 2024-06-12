from rest_framework.routers import SimpleRouter

from plant.plants.api.views import PlantsList

app_name = "plants"

router = SimpleRouter()
router.register("", PlantsList)

urlpatterns = router.urls
