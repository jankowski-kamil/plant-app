from django.urls import path
from plant.plants.api.views import PlantsList
from rest_framework.routers import SimpleRouter

app_name = "plants"

router = SimpleRouter()
router.register("", PlantsList)

urlpatterns = router.urls