from rest_framework.routers import SimpleRouter

from plant.notifications.api.views import NotificationListView,NotificationUserListView

app_name = "notifications"

router = SimpleRouter()
router.register("notifications", NotificationListView, basename="notifications")
router.register("user-notifications", NotificationUserListView, basename="user-notifications")


urlpatterns = router.urls
